from scripts.utils import get_account, deploy_mocks
from scripts.deploy import deploy_crowd_fund_contract


def fund(contract, value):
    tx = contract.fund({"from": get_account(),
                   "value": value})
    tx.wait(1)


def drain(contract):
    tx = contract.drain({"from": get_account()})
    tx.wait(1)


def main():
    contract = deploy_crowd_fund_contract()
    fund(contract, 10**17)
    drain(contract)
