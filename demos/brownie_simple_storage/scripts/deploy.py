from turtle import update
from brownie import accounts, config, SimpleStorage, network
import os


def deploy_simple_storage():
    # account = accounts[0]  # ganache
    # account = accounts.load("casafurix-account") #my own

    # account = accounts.add(os.getenv("PRIVATE_KEY"))
    # account = accounts.add(config["wallets"]["from_key"])
    # print(account)
    account = get_account()
    simple_storage = SimpleStorage.deploy(
        {"from": account}
    )  # this is a transaction function, hence the from argument
    stored_value = (
        simple_storage.retrieve()
    )  # this is a call/view function, hence, no need of argument
    print(stored_value)
    transaction = simple_storage.store(25, {"from": account})
    transaction.wait(1)
    updated_stored_value = simple_storage.retrieve()
    print(updated_stored_value)
    print(simple_storage)


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_simple_storage()
