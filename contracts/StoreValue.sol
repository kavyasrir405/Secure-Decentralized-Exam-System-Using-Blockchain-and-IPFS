pragma solidity >=0.4.22 <0.9.0;

contract StoreValue {
    uint private value;

    function set(uint v) public {
        value = v;
    }

    function get() public view returns (uint) {
        return value;
    }
}
