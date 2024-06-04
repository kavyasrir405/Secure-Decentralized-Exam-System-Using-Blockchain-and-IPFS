pragma solidity >=0.4.22 <0.9.0;

pragma experimental ABIEncoderV2; 

contract Quiz {
    struct Question {
        string question;
        string[] options;
        uint256 correctOptionIndex;
    }

    Question[] public questions;
    mapping(uint256 => address) public questionToOwner;

    event NewQuestion(uint256 questionId, string question);

    function addQuestion(string memory _question, string[] memory _options, uint256 _correctOptionIndex) public {
        require(_options.length >= 2, "Options length must be at least 2");
        require(_correctOptionIndex < _options.length, "Correct option index out of bounds");
        
        uint256 questionId = questions.length;
        questions.push(Question(_question, _options, _correctOptionIndex));
        questionToOwner[questionId] = msg.sender;

        emit NewQuestion(questionId, _question);
    }

    function getQuestion(uint256 _questionId) public view returns (string memory, string[] memory) {
        require(_questionId < questions.length, "Question id out of bounds");

        Question memory q = questions[_questionId];
        return (q.question, q.options);
    }

    function checkAnswer(uint256 _questionId, uint256 _selectedOptionIndex) public view returns (bool) {
        require(_questionId < questions.length, "Question id out of bounds");
        require(_selectedOptionIndex < questions[_questionId].options.length, "Selected option index out of bounds");

        return _selectedOptionIndex == questions[_questionId].correctOptionIndex;
    }
}
