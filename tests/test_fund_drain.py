import brownie.exceptions

from scripts.deploy import deploy_crowd_fund_contract
import pytest
from brownie import accounts
from scripts.fund_drain import fund, drain


def test_fund_drain():
    contract = deploy_crowd_fund_contract()
    value = 10 ** 17
    fund(contract, value)
    drain(contract)


def test_min_fund_value():
    contract = deploy_crowd_fund_contract()
    value = 1
    try:
        fund(contract, value)
    except brownie.exceptions.VirtualMachineError as ex:
        return
    pytest.fail("Exception was not thrown")


def test_only_owner_can_drain():
    contract = deploy_crowd_fund_contract()
    value = 10 ** 18
    fund(contract, value)
    try:
        contract.drain({"from": accounts.add()})
    except brownie.exceptions.VirtualMachineError as ex:
        return
    pytest.fail("Exception was not thrown")
