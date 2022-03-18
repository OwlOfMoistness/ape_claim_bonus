pragma solidity ^0.8.2;

import "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

interface IGrape {
	function claimTokens() external;
	function alphaClaimed(uint256) external view returns(bool);
	function betaClaimed(uint256) external view returns(bool);
	function gammaClaimed(uint256) external view returns(bool);
}

interface IClaim {
	function claim() external;
}

contract ApeClaimBonusManager {
	IGrape public constant GRAPE = IGrape(0x025C6da5BD0e6A5dd1350fda9e3B6a614B205a1F);
	IERC20 public constant APE = IERC20(0x4d224452801ACEd8B2F0aebE155379bb5D594381);
	IERC721 public constant ALPHA = IERC721(0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D);
	IERC721 public constant BETA = IERC721(0x60E4d786628Fea6478F785A6d7e704777c86a7c6);
	IERC721 public constant GAMMA = IERC721(0xba30E5F9Bb24caa003E9f2f0497Ad287FDF95623);

	uint256 constant ALPHA_SHARE = 10094 ether;
	uint256 constant BETA_SHARE = 2042 ether;
	uint256 constant GAMMA_SHARE = 856 ether;

	uint256 constant A_B_COMMS = 15;
	uint256 constant G_COMMS = 70;
	uint256 constant OUR_COMMS = 15;

	address public claimer;
	mapping(address => mapping(uint256 => address)) public assetToUser;

	function min(uint256 a, uint256 b) internal pure returns (uint256) {
		return a < b ? a : b;
	}
	function depositAlpha(uint256[] calldata _alphas) external {
		uint256 gammaBalance = GAMMA.balanceOf(address(this));
		uint256 toSwap = min(gammaBalance, _alphas.length);

		for (uint256 i = 0; i < toSwap; i++) {
			require(GRAPE.alphaClaimed(_alphas[i]), "Alpha already claimed");
			ALPHA.transferFrom(msg.sender, claimer, _alphas[i]);
			GAMMA.transferFrom(address(this), claimer, GAMMA.tokenOfOwnerByIndex(address(this), 0));
		}
		IClaim(claimer).claim();
		for (uint256 i = 0; i < toSwap; i++) {
			ALPHA.transferFrom(claimer, msg.sender, _alphas[i]);
			uint256 gammaTokenId = GAMMA.tokenOfOwnerByIndex(claimer, 0);
			address gammaOwner = assetToUser[address(GAMMA)][gammaTokenId];
			delete assetToUser[address(GAMMA)][gammaTokenId];
			GAMMA.transferFrom(claimer, gammaOwner, gammaTokenId);
			APE.transfer(gammaOwner, GAMMA_SHARE * G_COMMS / 100);
		}
		for (uint256 i = toSwap; i < _alphas.length; i++) {
			require(GRAPE.alphaClaimed(_alphas[i]), "Alpha already claimed");
			ALPHA.transferFrom(msg.sender, address(this), _alphas[i]);
			assetToUser[address(ALPHA)][_alphas[i]] = msg.sender;
		}
		APE.transfer(msg.sender, toSwap * (ALPHA_SHARE + GAMMA_SHARE * A_B_COMMS / 100));
	}

	function depositBeta(uint256[] calldata _betas) external {
		uint256 gammaBalance = GAMMA.balanceOf(address(this));
		uint256 toSwap = min(gammaBalance, _betas.length);

		for (uint256 i = 0; i < toSwap; i++) {
			require(GRAPE.betaClaimed(_betas[i]), "Beta already claimed");
			BETA.transferFrom(msg.sender, claimer, _betas[i]);
			GAMMA.transferFrom(address(this), claimer, GAMMA.tokenOfOwnerByIndex(address(this), 0));
		}
		IClaim(claimer).claim();
		for (uint256 i = 0; i < toSwap; i++) {
			BETA.transferFrom(claimer, msg.sender, _betas[i]);
			uint256 gammaTokenId = GAMMA.tokenOfOwnerByIndex(claimer, 0);
			address gammaOwner = assetToUser[address(GAMMA)][gammaTokenId];
			delete assetToUser[address(GAMMA)][gammaTokenId];
			GAMMA.transferFrom(claimer, gammaOwner, gammaTokenId);
			APE.transfer(gammaOwner, GAMMA_SHARE * G_COMMS / 100);
		}
		for (uint256 i = toSwap; i < _betas.length; i++) {
			require(GRAPE.betaClaimed(_betas[i]), "Beta already claimed");
			BETA.transferFrom(msg.sender, address(this), _betas[i]);
			assetToUser[address(BETA)][_betas[i]] = msg.sender;
		}
		APE.transfer(msg.sender, toSwap * (BETA_SHARE + GAMMA_SHARE * A_B_COMMS / 100));
	}

	function depositGamma(uint256[] calldata _gammas) external {
		uint256 alphaBalance = ALPHA.balanceOf(address(this));
		uint256 betaBalance = BETA.balanceOf(address(this));
		uint256 alphaToSwap = min(alphaBalance, _gammas.length);
		uint256 betaToSwap = min(betaBalance, _gammas.length - alphaToSwap);

		for (uint256 i = 0; i < alphaToSwap; i++) {
			require(GRAPE.gammaClaimed(_gammas[i]), "Gamma already claimed");
			GAMMA.transferFrom(msg.sender, claimer, _gammas[i]);
			ALPHA.transferFrom(address(this), claimer, ALPHA.tokenOfOwnerByIndex(address(this), 0));
		}
		for (uint256 i = 0; i < betaToSwap; i++) {
			require(GRAPE.gammaClaimed(_gammas[i + alphaToSwap]), "Gamma already claimed");
			GAMMA.transferFrom(msg.sender, claimer, _gammas[i + alphaToSwap]);
			BETA.transferFrom(address(this), claimer, BETA.tokenOfOwnerByIndex(address(this), 0));
		}
		IClaim(claimer).claim();
		for (uint256 i = 0; i < alphaToSwap; i++) {
			GAMMA.transferFrom(claimer, msg.sender, _gammas[i]);
			uint256 alphaTokenId = ALPHA.tokenOfOwnerByIndex(claimer, 0);
			address alphaOwner = assetToUser[address(ALPHA)][alphaTokenId];
			delete assetToUser[address(ALPHA)][alphaTokenId];
			ALPHA.transferFrom(claimer, alphaOwner, alphaTokenId);
			APE.transfer(alphaOwner, ALPHA_SHARE + GAMMA_SHARE * A_B_COMMS / 100);
		}
		for (uint256 i = 0; i < betaToSwap; i++) {
			GAMMA.transferFrom(claimer, msg.sender, _gammas[i + alphaToSwap]);
			uint256 betaTokenId = BETA.tokenOfOwnerByIndex(claimer, 0);
			address betaOwner = assetToUser[address(BETA)][betaTokenId];
			delete assetToUser[address(BETA)][betaTokenId];
			BETA.transferFrom(claimer, betaOwner, betaTokenId);
			APE.transfer(alphaOwner, BETA_SHARE + GAMMA_SHARE * A_B_COMMS / 100);
		}
		for (uint256 i = alphaToSwap + betaToSwap; i < _gammas.length; i++) {
			require(GRAPE.gammaClaimed(_gammas[i]), "Gamma already claimed");
			GAMMA.transferFrom(msg.sender, address(this), _gammas[i]);
			assetToUser[address(GAMMA)][_gammas[i]] = msg.sender;
		}
		APE.transfer(msg.sender, (alphaToSwap + betaToSwap) * (GAMMA_SHARE * G_COMMS / 100));
	}
}