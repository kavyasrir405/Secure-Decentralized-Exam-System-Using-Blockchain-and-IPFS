const Quiz = artifacts.require("Quiz");

contract("Quiz", (accounts) => {
  it("should add a new question", async () => {
    const quizInstance = await Quiz.deployed();

    const question = "What is 2 + 2?";
    const options = ["3", "4", "5"];
    const correctOptionIndex = 1;

    await quizInstance.addQuestion(question, options, correctOptionIndex);

    const addedQuestion = await quizInstance.getQuestion(0);

    assert.equal(addedQuestion[0], question, "Question was not added correctly");
    assert.deepEqual(addedQuestion[1], options, "Options were not added correctly");
  });

  it("should check answer correctly", async () => {
    const quizInstance = await Quiz.deployed();

    const question = "What is 2 + 2?";
    const options = ["3", "4", "5"];
    const correctOptionIndex = 1;
    const selectedOptionIndex = 1;

    await quizInstance.addQuestion(question, options, correctOptionIndex);

    const isCorrect = await quizInstance.checkAnswer(0, selectedOptionIndex);

    assert.isTrue(isCorrect, "Answer check failed");
  });
});
