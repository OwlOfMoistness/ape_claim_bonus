// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.2;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/IERC721Enumerable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";


contract ClaimGrapeMock is Ownable {
	
	uint256 public constant ALPHA_DISTRIBUTION_AMOUNT = 10094 ether;
	uint256 public constant BETA_DISTRIBUTION_AMOUNT = 2042 ether;
	uint256 public constant GAMMA_DISTRIBUTION_AMOUNT = 856 ether;

	IERC721Enumerable public alpha;
	IERC721Enumerable public beta;
	IERC721Enumerable public gamma;
	IERC20 public grapesToken;

	mapping(uint256 => bool) public alphaClaimed;
	mapping(uint256 => bool) public betaClaimed;
	mapping(uint256 => bool) public gammaClaimed;

	constructor(address a, address b, address g, address token) {
		alpha = IERC721Enumerable(a);
		beta = IERC721Enumerable(b);
		gamma = IERC721Enumerable(g);
		grapesToken = IERC20(token);
	}


	function claimTokens() external {
        require((beta.balanceOf(msg.sender) > 0 || alpha.balanceOf(msg.sender) > 0), "Nothing to claim");

        uint256 tokensToClaim;
        uint256 gammaToBeClaim;

        (tokensToClaim, gammaToBeClaim) = getClaimableTokenAmountAndGammaToClaim(msg.sender);

        for(uint256 i; i < alpha.balanceOf(msg.sender); ++i) {
            uint256 tokenId = alpha.tokenOfOwnerByIndex(msg.sender, i);
            if(!alphaClaimed[tokenId]) {
                alphaClaimed[tokenId] = true;
            }
        }

        for(uint256 i; i < beta.balanceOf(msg.sender); ++i) {
            uint256 tokenId = beta.tokenOfOwnerByIndex(msg.sender, i);
            if(!betaClaimed[tokenId]) {
                betaClaimed[tokenId] = true;
            }
        }

        uint256 currentGammaClaimed;
        for(uint256 i; i < gamma.balanceOf(msg.sender); ++i) {
            uint256 tokenId = gamma.tokenOfOwnerByIndex(msg.sender, i);
            if(!gammaClaimed[tokenId] && currentGammaClaimed < gammaToBeClaim) {
                gammaClaimed[tokenId] = true;
                currentGammaClaimed++;
            }
        }

        grapesToken.transfer(msg.sender, tokensToClaim);
    }

	function getClaimableTokenAmountAndGammaToClaim(address _account) private view returns (uint256, uint256)
    {
        uint256 unclaimedAlphaBalance;
        for(uint256 i; i < alpha.balanceOf(_account); ++i) {
            uint256 tokenId = alpha.tokenOfOwnerByIndex(_account, i);
            if(!alphaClaimed[tokenId]) {
                ++unclaimedAlphaBalance;
            }
        }
        uint256 unclaimedBetaBalance;
        for(uint256 i; i < beta.balanceOf(_account); ++i) {
            uint256 tokenId = beta.tokenOfOwnerByIndex(_account, i);
            if(!betaClaimed[tokenId]) {
                ++unclaimedBetaBalance;
            }
        }
        uint256 unclaimedGamaBalance;
        for(uint256 i; i < gamma.balanceOf(_account); ++i) {
            uint256 tokenId = gamma.tokenOfOwnerByIndex(_account, i);
            if(!gammaClaimed[tokenId]) {
                ++unclaimedGamaBalance;
            }
        }

        uint256 gammaToBeClaim = min(unclaimedAlphaBalance + unclaimedBetaBalance, unclaimedGamaBalance);
        uint256 tokensAmount = (unclaimedAlphaBalance * ALPHA_DISTRIBUTION_AMOUNT)
        + (unclaimedBetaBalance * BETA_DISTRIBUTION_AMOUNT) + (gammaToBeClaim * GAMMA_DISTRIBUTION_AMOUNT);

        return (tokensAmount, gammaToBeClaim);
    }

	function min(uint256 a, uint256 b) internal pure returns (uint256) {
		return a < b ? a : b;
	}
}