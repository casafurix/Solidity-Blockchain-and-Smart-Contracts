from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

with open("demos/web3_py_simple_storage/SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

install_solc("0.8.0")

# Compiling Solidity
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# for connecting to ganache
w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/5b472b1e7eb242f3936a732d81256279")
)
chain_id = 4
my_address = "0xe7fC62E6E48b18Da04003956c025f0DBd0745196"
private_key = os.getenv("PRIVATE_KEY")

# Creating the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Getting the latest transaction count
nonce = w3.eth.getTransactionCount(my_address)
# print(nonce)

# 1. Building a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)

# 2. Signing a transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# 3. Sending a transaction
print("Deploying contract...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Contract deployed!")


# For Working with a contract, we require: a) Contract Address b) Contract ABI
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# call -> simulate making the call and getting a return value (blue button in remix)
# transact -> actually make a state change (orange button in remix)

# initial value of favoriteNumber
print(simple_storage.functions.retrieve().call())


print("Updating contract...")
store_transaction = simple_storage.functions.store(25).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("Updated contract!")
# favoriteNumber after update
print(simple_storage.functions.retrieve().call())