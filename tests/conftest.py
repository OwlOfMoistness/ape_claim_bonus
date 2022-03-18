import pytest


# @pytest.fixture(scope="function", autouse=True)
# def shared_setup(fn_isolation):
#     pass


@pytest.fixture()
def minter(accounts):
    return accounts[0]

@pytest.fixture()
def alpha(interface):
    return interface.IERC721Enumerable('0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D')

@pytest.fixture()
def beta(interface):
    return interface.IERC721Enumerable('0x60E4d786628Fea6478F785A6d7e704777c86a7c6')

@pytest.fixture()
def gamma(interface):
    return interface.IERC721Enumerable('0xba30E5F9Bb24caa003E9f2f0497Ad287FDF95623')

@pytest.fixture()
def ape(interface):
    return interface.ERC20('0x4d224452801ACEd8B2F0aebE155379bb5D594381')

@pytest.fixture()
def manager(ApeClaimBonusManager, minter):
    return ApeClaimBonusManager.deploy({'from':minter})

@pytest.fixture()
def claimer(ApeClaimBonus, manager, minter):
    return ApeClaimBonus.deploy(manager, {'from':minter})

