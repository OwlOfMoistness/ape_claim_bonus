from brownie.test import given, strategy
from brownie import Wei, accounts, reverts
import brownie
import random
import pytest

@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass

# NOTICE: asset owners haven't claimed yet, tests will pass until they do so

def test_alpha_claim(manager_mock, ape_mock, alpha_mock, gamma_mock, minter, claimer_mock, claim_ape_mock, accounts):
	ape_mock.transfer(claim_ape_mock, '100000000 ether', {'from':minter})
	caller = {'from':minter}
	manager_mock.init(claimer_mock, caller)
	alpha_owner = accounts.at('0x98e711f31e49c2e50c1a290b6f2b1e493e43ea76', force=True)
	ao_bal = ape_mock.balanceOf(alpha_owner)
	alphas = [919,6768,6324,1226,4203,3982,2816,2591,2425,4347]
	for a in alphas:
		alpha_mock.mint(a, {'from':alpha_owner})
	ao_alpha_bal = alpha_mock.balanceOf(alpha_owner)
	gamma_owner = accounts.at('0x0449Bc01e1D8154A118c56aaA776272e94B45929', force=True)
	go_bal = ape_mock.balanceOf(gamma_owner)
	gammas = [2295,2699,9306,5682,4678,226,3655,9409,7131,5032]
	for a in gammas:
		gamma_mock.mint(a, {'from':gamma_owner})
	go_gamma_bal = gamma_mock.balanceOf(gamma_owner)

	alpha_mock.setApprovalForAll(manager_mock, True, {'from':alpha_owner})
	gamma_mock.setApprovalForAll(manager_mock, True, {'from':gamma_owner})

	manager_mock.depositGamma(gammas[:9], {'from':gamma_owner})
	assert gamma_mock.balanceOf(manager_mock) == len(gammas[:9])
	with reverts('!owner'):
		manager_mock.withdrawGamma(gammas[:9], {'from':minter})
	manager_mock.withdrawGamma(gammas[:9], {'from':gamma_owner})
	assert gamma_mock.balanceOf(manager_mock) == 0
	assert gamma_mock.balanceOf(gamma_owner) == go_gamma_bal
	manager_mock.depositGamma(gammas[:9], {'from':gamma_owner})

	manager_mock.depositAlpha(alphas[:3], {'from':alpha_owner})
	manager_mock.depositAlpha(alphas[3:6], {'from':alpha_owner})
	manager_mock.depositAlpha(alphas[6:], {'from':alpha_owner})
	assert gamma_mock.balanceOf(gamma_owner) == go_gamma_bal
	assert alpha_mock.balanceOf(alpha_owner) == ao_alpha_bal - 1
	assert alpha_mock.balanceOf(manager_mock) == 1
	assert ape_mock.balanceOf(alpha_owner) - ao_bal == len(alphas[:9]) * (Wei('10094 ether') + Wei('856 ether') * 45 // 100)
	assert ape_mock.balanceOf(gamma_owner) - go_bal == len(gammas[:9]) * (Wei('856 ether') * 45 // 100)
	assert ape_mock.balanceOf(manager_mock) == len(gammas[:9]) * (Wei('856 ether') * 10 // 100)


def test_beta_claim(manager_mock, ape_mock, beta_mock, gamma_mock, minter, claimer_mock, claim_ape_mock, accounts):
	ape_mock.transfer(claim_ape_mock, '100000000 ether', {'from':minter})

	caller = {'from':minter}
	manager_mock.init(claimer_mock, caller)
	beta_owner = accounts.at('0x65de7da4eba5ed248e3dc1c4d3e1e10abe96aadf', force=True)
	bo_bal = ape_mock.balanceOf(beta_owner)
	betas = [6304,5409,5330,3968,2900,2308,1169,115,18026,20734]
	for a in betas:
		beta_mock.mint(a, {'from':beta_owner})
	ao_beta_bal = beta_mock.balanceOf(beta_owner)
	gamma_owner = accounts.at('0x0449Bc01e1D8154A118c56aaA776272e94B45929', force=True)
	go_bal = ape_mock.balanceOf(gamma_owner)
	gammas = [2295,2699,9306,5682,4678,226,3655,9409,7131,5032]
	for a in gammas:
		gamma_mock.mint(a, {'from':gamma_owner})
	go_gamma_bal = gamma_mock.balanceOf(gamma_owner)

	beta_mock.setApprovalForAll(manager_mock, True, {'from':beta_owner})
	gamma_mock.setApprovalForAll(manager_mock, True, {'from':gamma_owner})

	manager_mock.depositGamma(gammas, {'from':gamma_owner})
	assert gamma_mock.balanceOf(manager_mock) == len(gammas)
	with reverts('!owner'):
		manager_mock.withdrawGamma(gammas, {'from':minter})
	manager_mock.withdrawGamma(gammas, {'from':gamma_owner})
	assert gamma_mock.balanceOf(manager_mock) == 0
	assert gamma_mock.balanceOf(gamma_owner) == go_gamma_bal
	manager_mock.depositGamma(gammas, {'from':gamma_owner})

	manager_mock.depositBeta(betas[:3], {'from':beta_owner})
	manager_mock.depositBeta(betas[3:6], {'from':beta_owner})
	manager_mock.depositBeta(betas[6:], {'from':beta_owner})
	assert gamma_mock.balanceOf(gamma_owner) == go_gamma_bal
	assert beta_mock.balanceOf(beta_owner) == ao_beta_bal
	assert ape_mock.balanceOf(beta_owner) - bo_bal == len(betas) * (Wei('2042 ether') + Wei('856 ether') * 45 // 100)
	assert ape_mock.balanceOf(gamma_owner) - go_bal == len(gammas) * (Wei('856 ether') * 45 // 100)
	assert ape_mock.balanceOf(manager_mock) == len(gammas) * (Wei('856 ether') * 10 // 100)

def test_gamma_claim(manager_mock, ape_mock, alpha_mock, beta_mock, gamma_mock, minter, claimer_mock, claim_ape_mock, accounts):
	ape_mock.transfer(claim_ape_mock, '100000000 ether', {'from':minter})

	caller = {'from':minter}
	manager_mock.init(claimer_mock, caller)
	alpha_owner = accounts.at('0x98e711f31e49c2e50c1a290b6f2b1e493e43ea76', force=True)
	ao_bal = ape_mock.balanceOf(alpha_owner)
	alphas = [919,6768,6324,1226,4203,3982,2816,2591,2425,4347]
	for a in alphas:
		alpha_mock.mint(a, {'from':alpha_owner})
	ao_alpha_bal = alpha_mock.balanceOf(alpha_owner)
	beta_owner = accounts.at('0x65de7da4eba5ed248e3dc1c4d3e1e10abe96aadf', force=True)
	bo_bal = ape_mock.balanceOf(beta_owner)
	ao_beta_bal = beta_mock.balanceOf(beta_owner)
	betas = [6304,5409,5330,3968,2900,2308,1169,115,18026,20734]
	for a in betas:
		beta_mock.mint(a, {'from':beta_owner})
	ao_beta_bal = beta_mock.balanceOf(beta_owner)
	gamma_owner = accounts.at('0x0449Bc01e1D8154A118c56aaA776272e94B45929', force=True)
	go_bal = ape_mock.balanceOf(gamma_owner)
	gammas = [2295,2699,9306,5682,4678,226,3655,9409,7131,5032]
	for a in gammas:
		gamma_mock.mint(a, {'from':gamma_owner})
	go_gamma_bal = gamma_mock.balanceOf(gamma_owner)

	alpha_mock.setApprovalForAll(manager_mock, True, {'from':alpha_owner})
	beta_mock.setApprovalForAll(manager_mock, True, {'from':beta_owner})
	gamma_mock.setApprovalForAll(manager_mock, True, {'from':gamma_owner})

	manager_mock.depositAlpha(alphas[:3], {'from':alpha_owner})
	assert alpha_mock.balanceOf(manager_mock) == len(alphas[:3])
	with reverts('!owner'):
		manager_mock.withdrawAlpha(alphas[:3], {'from':minter})
	manager_mock.withdrawAlpha(alphas[:3], {'from':alpha_owner})
	assert alpha_mock.balanceOf(manager_mock) == 0
	assert alpha_mock.balanceOf(alpha_owner) == ao_alpha_bal
	manager_mock.depositAlpha(alphas[:3], {'from':alpha_owner})

	manager_mock.depositBeta(betas[:3], {'from':beta_owner})
	assert beta_mock.balanceOf(manager_mock) == len(betas[:3])
	with reverts('!owner'):
		manager_mock.withdrawBeta(betas[:3], {'from':minter})
	manager_mock.withdrawBeta(betas[:3], {'from':beta_owner})
	assert beta_mock.balanceOf(manager_mock) == 0
	assert beta_mock.balanceOf(beta_owner) == ao_beta_bal
	manager_mock.depositBeta(betas[:3], {'from':beta_owner})

	manager_mock.depositGamma(gammas[:2], {'from':gamma_owner})
	manager_mock.depositGamma(gammas[2:4], {'from':gamma_owner})
	manager_mock.depositGamma(gammas[4:6], {'from':gamma_owner})
	assert gamma_mock.balanceOf(gamma_owner) == go_gamma_bal
	manager_mock.depositGamma(gammas[6:8], {'from':gamma_owner})
	assert gamma_mock.balanceOf(gamma_owner) == go_gamma_bal - 2
	assert beta_mock.balanceOf(beta_owner) == ao_beta_bal
	assert alpha_mock.balanceOf(alpha_owner) == ao_alpha_bal
	manager_mock.withdrawGamma(gammas[6:8], {'from':gamma_owner})
	assert gamma_mock.balanceOf(gamma_owner) == go_gamma_bal

	assert ape_mock.balanceOf(alpha_owner) - ao_bal == len(alphas[:3]) * (Wei('10094 ether') + Wei('856 ether') * 45 // 100)
	assert ape_mock.balanceOf(beta_owner) - bo_bal == len(betas[:3]) * (Wei('2042 ether') + Wei('856 ether') * 45 // 100)
	assert ape_mock.balanceOf(gamma_owner) - go_bal == len(gammas[:6]) * (Wei('856 ether') * 45 // 100)
	assert ape_mock.balanceOf(manager_mock) == len(gammas[:6]) * (Wei('856 ether') * 10 // 100)