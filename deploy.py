import json
from web3 import Web3
from dotenv import load_dotenv, set_key
import os

load_dotenv()

# Подключение к локальной сети Hardhat
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
assert w3.is_connected(), "Не удалось подключиться к Hardhat"

# Загрузка аккаунта
private_key = os.getenv("PRIVATE_KEY")
account = w3.eth.account.from_key(private_key)
w3.eth.default_account = account.address

# Загрузка ABI и bytecode
with open("artifacts/contracts/MyNFT.sol/MyNFT.json") as f:
    contract_json = json.load(f)
abi = contract_json["abi"]
bytecode = contract_json["bytecode"]

# Создание объекта контракта
MyNFT = w3.eth.contract(abi=abi, bytecode=bytecode)

# Построение транзакции развёртывания
tx = MyNFT.constructor().build_transaction({
    "from": account.address,
    "nonce": w3.eth.get_transaction_count(account.address),
    "gas": 3000000,
    "gasPrice": w3.eth.gas_price,
})

# Подпись и отправка
signed = account.sign_transaction(tx)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Контракт развёрнут по адресу: {receipt.contractAddress}")

# Запись адреса в .env, чтобы не копировать вручную
set_key(".env", "CONTRACT_ADDRESS", receipt.contractAddress, quote_mode="never")
print("CONTRACT_ADDRESS записан в .env")
