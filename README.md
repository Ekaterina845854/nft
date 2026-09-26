# ТЗ №8. «Простой NFT»

Упрощённый NFT-контракт (в духе ERC-721): любой адрес может выпустить (`mint`) токен с URI метаданных. Контракт разворачивается в локальной сети Hardhat, для взаимодействия используется Python и `web3.py`.

**Критерий сдачи:** вывести адрес владельца токена 0 и его URI.

## Результат выполнения

```text
> python deploy.py
Контракт развёрнут по адресу: 0x5FbDB2315678afecb367f032d93F642f64180aa3
CONTRACT_ADDRESS записан в .env

> python mint.py
Владелец токена 0: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
URI токена 0: ipfs://QmExample
```

`0xf39F…2266` — это Account #0 из `npx hardhat node`. Его приватный ключ указан в `.env`, поэтому он и развёртывает контракт, и вызывает `mint`.

## Структура проекта

```text
nft/
├── contracts/
│   └── MyNFT.sol         контракт из ТЗ
├── deploy.py             развёртывание контракта
├── mint.py               mint токена и чтение ownerOf / tokenURI (скрипт из ТЗ)
├── hardhat.config.js     конфигурация Hardhat (solc 0.8.24)
├── package.json          зависимость hardhat
├── requirements.txt      web3, python-dotenv
├── .env.example          шаблон .env
└── .gitignore            node_modules, artifacts, cache, .env
```

После компиляции появляется `artifacts/contracts/MyNFT.sol/MyNFT.json`. В нём лежат `abi` и `bytecode`, которые читают Python-скрипты.

## Предварительная подготовка (один раз)

1. Установить Node.js 18+ и Python 3.10+.
2. Установить зависимости:
   ```bash
   cd nft
   npm install                       # поставит hardhat из package.json
   pip install -r requirements.txt   # web3 и python-dotenv
   ```
3. *(Необязательно по ТЗ, из частей 1 и 3.4 методички)* Trust Wallet:
   - поставить расширение, создать кошелёк и записать seed-фразу на бумагу;
   - добавить сеть **Hardhat Local**: RPC `http://127.0.0.1:8545`, Chain ID `31337`, символ `ETH`;
   - импортировать Account #0 по приватному ключу из вывода `npx hardhat node`.

   Для сдачи ТЗ кошелёк не нужен: скрипты подписывают транзакции сами, ключом из `.env`.

> Проект создан без интерактивного `npx hardhat init`: конфиг `hardhat.config.js` написан вручную. Структура та же, что у шаблона «JavaScript project» (папки `scripts/` и `test/` не нужны и удалены). Взят Hardhat 2, потому что Hardhat 3 изменил `init` и формат проекта, а методичка рассчитана на Hardhat 2.

## Шаги запуска

Нужны два терминала, оба в папке `nft`.

**Терминал 1:** запустить локальный блокчейн (не закрывать до конца работы):

```bash
npx hardhat node
```

Hardhat выведет 20 аккаунтов по 10000 ETH. Адрес сети: `http://127.0.0.1:8545`, Chain ID: `31337`.

**Терминал 2:**

```bash
# 1. Компиляция
npx hardhat compile
# Compiled 1 Solidity file successfully

# 2. Создать .env из шаблона и вписать приватный ключ Account #0 из терминала 1
cp .env.example .env
# PRIVATE_KEY=0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80
# CONTRACT_ADDRESS=

# 3. Развёртывание: адрес контракта автоматически запишется в .env
python deploy.py

# 4. Mint NFT и проверка
python mint.py
```

> Ключ `0xac09…ff80` — стандартный публичный тестовый ключ Hardhat. Он годится только для локальной сети.

> При перезапуске `npx hardhat node` блокчейн сбрасывается. Тогда снова запустите `python deploy.py`, потом `python mint.py`.
> Если запустить `mint.py` повторно на том же контракте, появятся токены 1, 2, … Скрипт при этом по-прежнему печатает данные токена 0.

> Если в консоли Windows русский текст выводится криво, выполните `set PYTHONIOENCODING=utf-8` или `$env:PYTHONIOENCODING="utf-8"`.

## Содержание: Python-скрипты

### `deploy.py`: развёртывание

В ТЗ №8 скрипта развёртывания нет, поэтому он сделан по образцу `deploy.py` из ТЗ №1.

1. Подключается к `http://127.0.0.1:8545` и проверяет соединение (`w3.is_connected()`).
2. Создаёт аккаунт из `PRIVATE_KEY` (`w3.eth.account.from_key`).
3. Загружает `abi` и `bytecode` из `artifacts/contracts/MyNFT.sol/MyNFT.json`.
4. Строит транзакцию `MyNFT.constructor().build_transaction({...})` с полями `from`, `nonce`, `gas`, `gasPrice`.
5. Подписывает её (`account.sign_transaction`), отправляет (`send_raw_transaction`) и ждёт чек (`wait_for_transaction_receipt`).
6. Печатает `receipt.contractAddress` и записывает его в `.env` через `dotenv.set_key` (чтобы не писать вручную)

### `mint.py`: скрипт из ТЗ

1. Подключает уже развёрнутый контракт по `CONTRACT_ADDRESS` и ABI.
2. Вызывает `contract.functions.mint("ipfs://QmExample")`
3. После подтверждения читает данные через `.call()`, то есть без транзакции и без газа:
   - `ownerOf(0)` возвращает владельца токена 0;
   - `tokenURI(0)` возвращает URI токена 0.