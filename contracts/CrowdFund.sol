//SPDX-License-Identifier:MIT
pragma solidity 0.8.0;
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
contract CrowdFund{

    mapping(address => uint256) private addressToFundsMapping;
    address[] private addresses;
    address priceFeedAddress;

    address owner;

    constructor(address _priceFeed){
        owner = msg.sender;
        priceFeedAddress = _priceFeed;
    }

    modifier onlyOwner{
        require(msg.sender == owner);
        _;
    }

    function fund() public payable {
        require(getEtherUsdValue(msg.value) >= 10);
        addressToFundsMapping[msg.sender] = msg.value;
        addresses.push(msg.sender);
    }

    function drain() payable onlyOwner public {
        require(payable(msg.sender).send(address(this).balance));
        for (uint i=0; i < addresses.length; i++) {
            addressToFundsMapping[addresses[i]] = 0;
        }
        addresses = new address[](0);

    }

    function getEtherUsdValue(uint256 _ethAmount) public view returns (uint) {
        AggregatorV3Interface _priceFeed = AggregatorV3Interface(priceFeedAddress);
        (
            /*uint80 roundID*/,
            int price,
            /*uint startedAt*/,
            /*uint timeStamp*/,
            /*uint80 answeredInRound*/
        ) = _priceFeed.latestRoundData();
        return (uint(price)*_ethAmount)/(10**26);
    }
}