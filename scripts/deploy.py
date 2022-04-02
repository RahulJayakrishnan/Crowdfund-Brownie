from brownie import config, accounts, network, CrowdFund, MockV3Aggregator
from scripts.utils import get_account, deploy_mocks


def deploy_crowd_fund_contract():
    account = get_account()
    if network.show_active() != "development":
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1]
    crowd_fund = CrowdFund.deploy(price_feed_address, {"from": account},
                                  publish_source=config["networks"][network.show_active()].get("verify"))
    print(f"Created contract {crowd_fund.address}")
    return crowd_fund


def main():
    deploy_crowd_fund_contract()
