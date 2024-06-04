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
        "inputs": [{"name": "_quizName", "type": "string"}],
        "name": "createQuiz",
        "outputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {"name": "_quizId", "type": "uint256"},
            {"name": "_questionText", "type": "string"},
            {"name": "_assignedMarks", "type": "uint256"}
        ],
        "name": "addQuestion",
        "outputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [{"name": "_quizId", "type": "uint256"}],
        "name": "getQuiz",
        "outputs": [
            {"name": "", "type": "string"},
            {"name": "", "type": "uint256"}
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [
            {"name": "_quizId", "type": "uint256"},
            {"name": "_questionId", "type": "uint256"}
        ],
        "name": "getQuestion",
        "outputs": [
            {"name": "", "type": "string"},
            {"name": "", "type": "uint256"}
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "getQuizCount",
        "outputs": [
            {"name": "", "type": "uint256"}
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    }
];

const contractAddress = '0xDcBB5A881394e0F4E5370967Cfd44C479041F2d0'; // Replace with your contract's address
const contract = new web3.eth.Contract(contractABI, contractAddress);

async function createQuiz() {
    const accounts = await web3.eth.getAccounts();
    const quizName = document.getElementById('quizName').value;
    contract.methods.createQuiz(quizName).send({ from: accounts[0] })
        .then(() => {
            console.log('Quiz created successfully.');
        })
        .catch((error) => {
            console.error('Error creating quiz:', error);
        });
}


async function addQuestion() {
    const accounts = await web3.eth.getAccounts();
    const quizCount = await contract.methods.getQuizCount().call();
    const latestQuizId = quizCount - 1;
    const questionText = document.getElementById('questionText').value;
    const assignedMarks = document.getElementById('assignedMarks').value;
    contract.methods.addQuestion(latestQuizId, questionText, assignedMarks).send({ from: accounts[0] })
        .then(() => {
            console.log('Question added successfully.');
        })
        .catch((error) => {
            console.error('Error adding question:', error);
        });
}


document.getElementById('quizForm').addEventListener('submit', (event) => {
    event.preventDefault();
    createQuiz();
});

document.getElementById('questionForm').addEventListener('submit', (event) => {
    event.preventDefault();
    addQuestion();
});
