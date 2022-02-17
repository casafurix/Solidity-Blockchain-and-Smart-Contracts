from brownie import SimpleStorage, accounts, config


def read_contract():
    simple_storage = SimpleStorage[
        -1
    ]  # [-1] gives us the most recent deployment, [0] gives the very first deployment
    # automatically knows the abi and address automatically
    print(simple_storage.retrieve())


def main():
    read_contract()
