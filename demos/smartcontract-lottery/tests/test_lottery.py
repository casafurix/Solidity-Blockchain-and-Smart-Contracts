# 50/2728.52 = 0.01832 ETH entry fee, basically 50 USD = 0.01832 ETH
# 1.832e+16 wei
from brownie import Lottery, accounts, config, network
from web3 import Web3


def test_get_entrance_fee():
    account = accounts[0]
    lottery = Lottery.deploy(
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        {"from": account},
    )
    # assert lottery.getEntranceFee() > Web3.toWei(0.018, "ether")
    # assert lottery.getEntranceFee() < Web3.toWei(0.02, "ether")
