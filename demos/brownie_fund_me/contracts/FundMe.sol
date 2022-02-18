// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;
    address public owner;

    constructor() public {
        owner = msg.sender;
    }

    function fund() public payable {
        // $50
        uint256 minimumUSD = 50 * 10**18;

        require(
            getConversionRate(msg.value) >= minimumUSD,
            "You need to spend more ETH, you cheapo!"
        );

        addressToAmountFunded[msg.sender] += msg.value;

        funders.push(msg.sender);
    }

    function getVersion() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
        );
        priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
        );
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 10000000000);
    }

    // 2929.33944412

    // 1000000000 = $2929339444120,000000000000000000 -> incorrect, so we divide that 10^18 term while returning
    // 1000000000 = $2929339444120 -> this number has 18 decimals as well.
    // so we further divide, (decimals cannot be shown in Solana): 1 Gwei = $0.000002929339444120
    // to verify, 0.000002929339444120 * 1000000000 = $2929.33944412 (price of 1 ETH in USD; 13 Feb, 2022)
    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        uint256 ethAmountinUSD = (ethPrice * ethAmount) / 1000000000000000000; //extra 10^18 term has to be divided, as 1 eth = 10^18 wei
        return ethAmountinUSD;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "ONLY OWNER CAN WITHDRAW, THIEF SPOTTED!");
        _;
    }

    function withdraw() public payable onlyOwner {
        // only want the contract owner/admin
        payable(msg.sender).transfer(address(this).balance);

        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }
        funders = new address[](0);
    }
}
