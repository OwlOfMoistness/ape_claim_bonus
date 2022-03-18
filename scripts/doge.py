from brownie import (
    interface,
    accounts,
    chain,
    interface,
    Wei,
		web3,Contract
)


def main():
	grape = Contract('0x025C6da5BD0e6A5dd1350fda9e3B6a614B205a1F')
	claimed = 0
	for i in range(1,9500):
		print(i, end='\r')
		if grape.gammaClaimed(i):
			claimed += 1

	print(f'Claimed: {claimed}')
	print(f'Remaining: {9500 - claimed}')