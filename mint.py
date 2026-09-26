import json
from web3 import Web3
from dotenv import load_dotenv
import os

load_dotenv()
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
private_key = os.getenv("PRIVATE_KEY")
account = w3.eth.account.from_key(private_key)

with open("artifacts/contracts/MyNFT.sol/MyNFT.json") as f:
    contract_json = json.load(f)

contract = w3.eth.contract(address=os.getenv("CONTRACT_ADDRESS"), abi=contract_json["abi"])

#  вызов функции mint с URI метаданных.
tx = contract.functions.mint("ipfs://QmExample").build_transaction({
    "from": account.address,
    "nonce": w3.eth.get_transaction_count(account.address),
    "gas": 300000,
    "gasPrice": w3.eth.gas_price,
})
signed = account.sign_transaction(tx)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
w3.eth.wait_for_transaction_receipt(tx_hash)

print(f"Владелец токена 0: {contract.functions.ownerOf(0).call()}")
print(f"URI токена 0: {contract.functions.tokenURI(0).call()}")
