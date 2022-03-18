pragma solidity ^0.8.2;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {IGrape} from "./ApeClaimBonusManager.sol";

contract ApeClaimBonus {
	IGrape public constant GRAPE = IGrape(0x025C6da5BD0e6A5dd1350fda9e3B6a614B205a1F);
	IERC721 public constant ALPHA = IERC721(0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D);
	IERC721 public constant BETA = IERC721(0x60E4d786628Fea6478F785A6d7e704777c86a7c6);
	IERC721 public constant GAMMA = IERC721(0xba30E5F9Bb24caa003E9f2f0497Ad287FDF95623);

	address public manager;

	constructor(address _manager) {
		manager = _manager;
		ALPHA.setApprovalForAll(_manager, true);
		BETA.setApprovalForAll(_manager, true);
		GAMMA.setApprovalForAll(_manager, true);
	}

	function claim() external {
		require(msg.sender == manager);
		GRAPE.claimTokens();
		APE.transfer(msg.sender, APE.balanceOf(address(this)));
	}
}