from brownie import (
    interface,
    accounts,
    chain,
    interface,
    Wei,
		web3,
		Contract,
	MockNft,
	TokenNft,
	ClaimGrapeMock,
	ApeClaimBonusManager,
	ApeClaimBonus
)



def deploy_rinkeby():
	minter = accounts.load('moist', '\0')

	# alpha = MockNft.deploy("ape", "BAYC", {'from':minter}, publish_source=False)
	# beta = MockNft.deploy("mutant", "mayc", {'from':minter})
	# gamma = MockNft.deploy("doge", "BAKC", {'from':minter})

	alpha = MockNft.at('0xdED0C21B405fE18F5eaB216E352bec1f281156fC')
	beta = MockNft.at('0x08DC7dAF7ee67958c3c96A2C730653117c0870dE')
	gamma = MockNft.at('0x34CC0988a2DAFb2b5270334BC7C84378f40Fa34D')

	# ape = TokenNft.deploy({'from':minter}, publish_source=False)
	# claim_ape = ClaimGrapeMock.deploy(alpha, beta, gamma, ape, {'from':minter}, publish_source=False)
	ape = TokenNft.at('0x893eE938C9fdC99Cc759f9375abdced6F97B1BE9')
	claim_ape = ClaimGrapeMock.at('0x6771AC0b98A3200576bAC4eEde254D9e9103c66D')

	# manager = ApeClaimBonusManager.deploy(ape, claim_ape, alpha, beta, gamma, {'from':minter})
	# claimer = ApeClaimBonus.deploy(manager, ape, claim_ape, alpha, beta, gamma, {'from':minter})
	# manager.init(claimer, {'from':minter})

	manager = ApeClaimBonusManager.at('0x2e716F6450C923936ba71a68a1f7B68827B3c3e2')
	claimer = ApeClaimBonus.at('0x70BC873EBFf2D3d8e2A8e18AA20f305585117d28')
	manager.init(claimer, {'from':minter})


	ape.transfer(claim_ape, '100000000 ether', {'from':minter})

	receiver = '0x4d69A96Ca90EBa1716812297139C9b616d8fc8aA'
	minter.transfer(to=receiver, amount='5 ether')

	alphas = [919,6768,6324,1226,4203,3982,2816,2591,2425,4347]
	alpha.mintMany(alphas, receiver, {'from':minter})

	betas = [6304,5409,5330,3968,2900,2308,1169,115,18026,20734]
	beta.mintMany(betas, receiver, {'from':minter})

	gammas = [2295,2699,9306,5682,4678,226,3655,9409,7131,5032]
	gamma.mintMany(gammas, receiver, {'from':minter})

	url = 'https://goerli.etherscan.io/address/'
	print(f'alpha: {url}{alpha.address}')
	print(f'beta: {url}{beta.address}')
	print(f'gamma: {url}{gamma.address}')
	print(f'ape: {url}{ape.address}')
	print(f'manager: {url}{manager.address}')
	print(f'claim_ape: {url}{claim_ape.address}')
