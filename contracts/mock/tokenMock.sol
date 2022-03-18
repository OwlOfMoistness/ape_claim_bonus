// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.2;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract TokenNft is ERC20("APE", "APE") {

	constructor(){
		_mint(msg.sender, 1_000_000_000 ether);
	}

}