// Connect to Ethereum network
if (window.ethereum) {
    window.web3 = new Web3(window.ethereum);
    window.ethereum.enable();
} else {
    console.error('No Ethereum provider detected. Install MetaMask or another wallet.');
}

// Contract ABI and Address
const contractABI = [
    {
        "constant": false,
        "inputs": [{"name": "v", "type": "uint256"}],
        "name": "set",
        "outputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "get",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    }
];

const contractAddress = '0x8DC141c757D21f8e5d7d5a40b5a3A913705D32E2'; // Replace with your contract's address
const contract = new web3.eth.Contract(contractABI, contractAddress);

document.getElementById('valueForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const accounts = await web3.eth.getAccounts();
    const value = document.getElementById('valueInput').value;
    contract.methods.set(value).send({ from: accounts[0] })
        .then(() => {
            console.log('Value set successfully.');
        })
        .catch((error) => {
            console.error('Error setting value:', error);
        });
});

document.getElementById('getValueButton').addEventListener('click', () => {
    contract.methods.get().call()
        .then((value) => {
            document.getElementById('storedValue').innerText = value;
        })
        .catch((error) => {
            console.error('Error getting value:', error);
        });
});
