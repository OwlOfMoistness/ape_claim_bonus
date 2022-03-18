// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.2;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";

contract MockNft is ERC721Enumerable {

	constructor(string memory _name, string memory _symbol) ERC721(_name, _symbol) {

	}

	function mint(uint256 _id) external {
		_mint(msg.sender, _id);
	}
}