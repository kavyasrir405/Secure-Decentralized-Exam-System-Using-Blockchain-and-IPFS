// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;
pragma experimental ABIEncoderV2;

contract Create_quiz {
    struct Question {
        string text;
        uint assignedMarks;
    }

    struct QuizData {
        string quizName;
        Question[] questions;
        mapping(uint => bool) questionExists;
        mapping(uint => string) answerImages; // Mapping to store answer images URLs or IPFS CIDs
    }

    mapping(uint => QuizData) private quizzes;
    uint private quizCount = 0;

    // Event for quiz creation
    event QuizCreated(uint quizId, string quizName);

    // Function to create a quiz
    function createQuiz(string memory _quizName) public {
        quizzes[quizCount].quizName = _quizName;
        emit QuizCreated(quizCount, _quizName);
        quizCount++;
    }

    // Function to add a question to a quiz
    function addQuestion(uint _quizId, string memory _questionText, uint _assignedMarks) public {
        require(_quizId < quizCount, "Quiz does not exist");
        quizzes[_quizId].questions.push(Question(_questionText, _assignedMarks));
        quizzes[_quizId].questionExists[quizzes[_quizId].questions.length - 1] = true;
    }

    // Function to get quiz details
    function getQuiz(uint _quizId) public view returns (string memory, uint) {
        require(_quizId < quizCount, "Quiz does not exist");
        return (quizzes[_quizId].quizName, quizzes[_quizId].questions.length);
    }

    // Function to get a question from a quiz
    function getQuestion(uint _quizId, uint _questionId) public view returns (string memory, uint) {
        require(_quizId < quizCount, "Quiz does not exist");
        require(quizzes[_quizId].questionExists[_questionId], "Question does not exist");
        Question storage question = quizzes[_quizId].questions[_questionId];
        return (question.text, question.assignedMarks);
    }

    // Function to get all quiz names and IDs
    function getAllQuizzes() public view returns (string[] memory, uint[] memory) {
        string[] memory names = new string[](quizCount);
        uint[] memory ids = new uint[](quizCount);
        for (uint i = 0; i < quizCount; i++) {
            names[i] = quizzes[i].quizName;
            ids[i] = i;
        }
        return (names, ids);
    }

    // New function to get the quiz count
    function getQuizCount() public view returns (uint) {
        return quizCount;
    }

    // New function to submit an answer image (IPFS CID)
    function submitAnswer(uint _quizId, uint _questionId, string memory _imageCid) public {
        require(_quizId < quizCount, "Quiz does not exist");
        require(quizzes[_quizId].questionExists[_questionId], "Question does not exist");
        quizzes[_quizId].answerImages[_questionId] = _imageCid;
    }

    // New function to get the submitted answer image (IPFS CID)
    function getAnswerImage(uint _quizId, uint _questionId) public view returns (string memory) {
        require(_quizId < quizCount, "Quiz does not exist");
        require(quizzes[_quizId].questionExists[_questionId], "Question does not exist");
        return quizzes[_quizId].answerImages[_questionId];
    }
}
