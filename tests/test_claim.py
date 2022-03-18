from brownie.test import given, strategy
from brownie import Wei, accounts, reverts
import brownie
import random
import pytest

@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass

# NOTICE: asset owners haven't claimed yet, tests will pass until they do so

def test_alpha_claim(manager, ape, alpha, gamma, minter, claimer, accounts):
	caller = {'from':minter}
	manager.init(claimer, caller)
	alpha_owner = accounts.at('0x98e711f31e49c2e50c1a290b6f2b1e493e43ea76', force=True)
	ao_bal = ape.balanceOf(alpha_owner)
	ao_alpha_bal = alpha.balanceOf(alpha_owner)
	alphas = [919,6768,6324,1226,4203,3982,2816,2591,2425,4347]
	gamma_owner = accounts.at('0x0449Bc01e1D8154A118c56aaA776272e94B45929', force=True)
	go_bal = ape.balanceOf(gamma_owner)
	go_gamma_bal = gamma.balanceOf(gamma_owner)
	gammas = [2295,2699,9306,5682,4678,226,3655,9409,7131,5032]

	alpha.setApprovalForAll(manager, True, {'from':alpha_owner})
	gamma.setApprovalForAll(manager, True, {'from':gamma_owner})

	manager.depositGamma(gammas[:9], {'from':gamma_owner})
	assert gamma.balanceOf(manager) == len(gammas[:9])
	with reverts('!owner'):
		manager.withdrawGamma(gammas[:9], {'from':minter})
	manager.withdrawGamma(gammas[:9], {'from':gamma_owner})
	assert gamma.balanceOf(manager) == 0
	assert gamma.balanceOf(gamma_owner) == go_gamma_bal
	manager.depositGamma(gammas[:9], {'from':gamma_owner})

	manager.depositAlpha(alphas[:3], {'from':alpha_owner})
	manager.depositAlpha(alphas[3:6], {'from':alpha_owner})
	manager.depositAlpha(alphas[6:], {'from':alpha_owner})
	assert gamma.balanceOf(gamma_owner) == go_gamma_bal
	assert alpha.balanceOf(alpha_owner) == ao_alpha_bal - 1
	assert alpha.balanceOf(manager) == 1
	assert ape.balanceOf(alpha_owner) - ao_bal == len(alphas[:9]) * (Wei('10094 ether') + Wei('856 ether') * 15 // 100)
	assert ape.balanceOf(gamma_owner) - go_bal == len(gammas[:9]) * (Wei('856 ether') * 70 // 100)
	assert ape.balanceOf(manager) == len(gammas[:9]) * (Wei('856 ether') * 15 // 100)


def test_beta_claim(manager, ape, beta, gamma, minter, claimer, accounts):
	caller = {'from':minter}
	manager.init(claimer, caller)
	beta_owner = accounts.at('0x65de7da4eba5ed248e3dc1c4d3e1e10abe96aadf', force=True)
	bo_bal = ape.balanceOf(beta_owner)
	ao_beta_bal = beta.balanceOf(beta_owner)
	betas = [6304,5409,5330,3968,2900,2308,1169,115,18026,20734]
	gamma_owner = accounts.at('0x0449Bc01e1D8154A118c56aaA776272e94B45929', force=True)
	go_bal = ape.balanceOf(gamma_owner)
	go_gamma_bal = gamma.balanceOf(gamma_owner)
	gammas = [2295,2699,9306,5682,4678,226,3655,9409,7131,5032]

	beta.setApprovalForAll(manager, True, {'from':beta_owner})
	gamma.setApprovalForAll(manager, True, {'from':gamma_owner})

	manager.depositGamma(gammas, {'from':gamma_owner})
	assert gamma.balanceOf(manager) == len(gammas)
	with reverts('!owner'):
		manager.withdrawGamma(gammas, {'from':minter})
	manager.withdrawGamma(gammas, {'from':gamma_owner})
	assert gamma.balanceOf(manager) == 0
	assert gamma.balanceOf(gamma_owner) == go_gamma_bal
	manager.depositGamma(gammas, {'from':gamma_owner})

	manager.depositBeta(betas[:3], {'from':beta_owner})
	manager.depositBeta(betas[3:6], {'from':beta_owner})
	manager.depositBeta(betas[6:], {'from':beta_owner})
	assert gamma.balanceOf(gamma_owner) == go_gamma_bal
	assert beta.balanceOf(beta_owner) == ao_beta_bal
	assert ape.balanceOf(beta_owner) - bo_bal == len(betas) * (Wei('2042 ether') + Wei('856 ether') * 15 // 100)
	assert ape.balanceOf(gamma_owner) - go_bal == len(gammas) * (Wei('856 ether') * 70 // 100)
	assert ape.balanceOf(manager) == len(gammas) * (Wei('856 ether') * 15 // 100)

def test_gamma_claim(manager, ape, alpha, beta, gamma, minter, claimer, accounts):
	caller = {'from':minter}
	manager.init(claimer, caller)
	alpha_owner = accounts.at('0x98e711f31e49c2e50c1a290b6f2b1e493e43ea76', force=True)
	ao_bal = ape.balanceOf(alpha_owner)
	ao_alpha_bal = alpha.balanceOf(alpha_owner)
	alphas = [919,6768,6324,1226,4203,3982,2816,2591,2425,4347]
	beta_owner = accounts.at('0x65de7da4eba5ed248e3dc1c4d3e1e10abe96aadf', force=True)
	bo_bal = ape.balanceOf(beta_owner)
	ao_beta_bal = beta.balanceOf(beta_owner)
	betas = [6304,5409,5330,3968,2900,2308,1169,115,18026,20734]
	gamma_owner = accounts.at('0x0449Bc01e1D8154A118c56aaA776272e94B45929', force=True)
	go_bal = ape.balanceOf(gamma_owner)
	go_gamma_bal = gamma.balanceOf(gamma_owner)
	gammas = [2295,2699,9306,5682,4678,226,3655,9409,7131,5032]

	alpha.setApprovalForAll(manager, True, {'from':alpha_owner})
	beta.setApprovalForAll(manager, True, {'from':beta_owner})
	gamma.setApprovalForAll(manager, True, {'from':gamma_owner})

	manager.depositAlpha(alphas[:3], {'from':alpha_owner})
	assert alpha.balanceOf(manager) == len(alphas[:3])
	with reverts('!owner'):
		manager.withdrawAlpha(alphas[:3], {'from':minter})
	manager.withdrawAlpha(alphas[:3], {'from':alpha_owner})
	assert alpha.balanceOf(manager) == 0
	assert alpha.balanceOf(alpha_owner) == ao_alpha_bal
	manager.depositAlpha(alphas[:3], {'from':alpha_owner})

	manager.depositBeta(betas[:3], {'from':beta_owner})
	assert beta.balanceOf(manager) == len(betas[:3])
	with reverts('!owner'):
		manager.withdrawBeta(betas[:3], {'from':minter})
	manager.withdrawBeta(betas[:3], {'from':beta_owner})
	assert beta.balanceOf(manager) == 0
	assert beta.balanceOf(beta_owner) == ao_beta_bal
	manager.depositBeta(betas[:3], {'from':beta_owner})

	manager.depositGamma(gammas[:2], {'from':gamma_owner})
	manager.depositGamma(gammas[2:4], {'from':gamma_owner})
	manager.depositGamma(gammas[4:6], {'from':gamma_owner})
	assert gamma.balanceOf(gamma_owner) == go_gamma_bal
	manager.depositGamma(gammas[6:8], {'from':gamma_owner})
	assert gamma.balanceOf(gamma_owner) == go_gamma_bal - 2
	assert beta.balanceOf(beta_owner) == ao_beta_bal
	assert alpha.balanceOf(alpha_owner) == ao_alpha_bal
	manager.withdrawGamma(gammas[6:8], {'from':gamma_owner})
	assert gamma.balanceOf(gamma_owner) == go_gamma_bal

	assert ape.balanceOf(alpha_owner) - ao_bal == len(alphas[:3]) * (Wei('10094 ether') + Wei('856 ether') * 15 // 100)
	assert ape.balanceOf(beta_owner) - bo_bal == len(betas[:3]) * (Wei('2042 ether') + Wei('856 ether') * 15 // 100)
	assert ape.balanceOf(gamma_owner) - go_bal == len(gammas[:6]) * (Wei('856 ether') * 70 // 100)
	assert ape.balanceOf(manager) == len(gammas[:6]) * (Wei('856 ether') * 15 // 100)