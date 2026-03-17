// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CarbonCredit {
    struct Credit {
        string company;
        uint256 amount;
        uint256 timestamp;
    }

    Credit[] public credits;

    // Carbon credit add karne ke liye function
    function addCredit(string memory _company, uint256 _amount) public {
        credits.push(Credit(_company, _amount, block.timestamp));
    }

    // Saare credits dekhne ke liye function
    function getCredits() public view returns (Credit[] memory) {
        return credits;
    }
}