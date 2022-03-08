from scripts.helpful_scripts import get_account
from brownie import network, config, interface
from scripts.get_weth import get_weth
from web3 import Web3

# 0.1
amount = Web3.toWei(0.1, "ether")


def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in ["mainnet-fork"]:
        get_weth()
    # ABI
    # address
    lending_pool = get_lending_pool()
    # approve sending out ERC20 tokens
    approve_erc20(lending_pool.address, amount, erc20_address, account)
    print("Depositing...")
    tx = lending_pool.deposit(
        erc20_address, amount, account.address, 0, {"from": account}
    )
    tx.wait(1)
    print("Deposited!")
    # how much can I borrow?
    borrowable_eth, total_debt = get_borrowable_data(lending_pool, account)
    print("Let's borrow!")
    # DAI in terms of ETH
    dai_eth_price = get_asset_price(
        config["networks"][network.show_active()]["dai_eth_price_feed"]
    )
    # borrowable_eth -> borrowable_dai * 95%, as a safety measure from getting liquidated
    amount_dai_to_borrow = (1 / dai_eth_price) * (borrowable_eth * 0.95)
    print(f"We are going to borrow {amount_dai_to_borrow} DAI!")
    # now, we will borrow
    dai_address = config["networks"][network.show_active()]["dai_token"]
    borrow_tx = lending_pool.borrow(
        dai_address,
        Web3.toWei(amount_dai_to_borrow, "ether"),
        1,
        0,
        account.address,
        {"from": account},
    )
    borrow_tx.wait(1)
    print("We borrowed some DAI!")
    get_borrowable_data(lending_pool, account)
    # repay time!
    # repay_all(Web3.toWei(amount_dai_to_borrow, "ether"), lending_pool, account)


def get_lending_pool():
    # ABI
    # address
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    # ABI
    # address - check!
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool


def approve_erc20(spender, amount, erc20_address, account):
    # ABI
    # address
    print("Approving ERC20 token...")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("Approved!")
    return tx


def get_borrowable_data(lending_pool, account):
    (
        total_collateral_eth,
        total_debt_eth,
        available_borrow_eth,
        current_liquidation_threshold,
        ltv,
        health_factor,
    ) = lending_pool.getUserAccountData(account.address)
    available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")
    total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")
    print(f"You have {total_collateral_eth} worth of ETH deposited!")
    print(f"You have {total_debt_eth} worth of ETH borrowed!")
    print(f"You can borrow {available_borrow_eth} worth of ETH!")
    return (float(available_borrow_eth), float(total_debt_eth))


def get_asset_price():
    # ABI
    # address
    # dai_eth_price_feed = interface.AggregatorV3Interface(price_feed_address)
    # latest_price = dai_eth_price_feed.latestRoundData()[1]
    # converted_latest_price = Web3.fromWei(latest_price, "ether")
    # print(f"The DAI/ETH price is {converted_latest_price}!")
    # return float(converted_latest_price)
    # 0.000378190716147148
    dai_eth_price_feed = interface.AggregatorV3Interface(
        config["networks"][network.show_active()]["dai_eth_price_feed"]
    )
    latest_price = Web3.fromWei(dai_eth_price_feed.latestRoundData()[1], "ether")
    print(f"The DAI/ETH price is {latest_price}")
    return float(latest_price)


def repay_all(amount, lending_pool, account):
    # first we call the approve function
    approve_erc20(
        lending_pool,
        Web3.toWei(amount, "ether"),
        config["networks"][network.show_active()]["dai_token"],
        account,
    )
    repay_tx = lending_pool.repay(
        config["networks"][network.show_active()]["dai_token"],
        amount,
        1,
        account.address,
        {"from": account},
    )
    repay_tx.wait(1)
    print("Repaid!")
    print(
        "We just deposited, borrowed and repaid with Aave, Brownie, and Chainlink! Hurray!"
    )