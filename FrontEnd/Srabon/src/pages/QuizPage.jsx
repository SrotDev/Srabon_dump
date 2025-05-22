import React, { useState } from 'react';
import { useNavigate, useLocation, useParams } from 'react-router-dom';

const QuizPage = () => {
  const { name } = useParams();
  const location = useLocation();
  const course = location.state?.course; // Receive the course data via props
  const [selectedAnswers, setSelectedAnswers] = useState(new Array(6).fill(null)); // Track selected answers
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0); // Current question index
  const navigate = useNavigate();

  if (!course) {
    return <div className="loading">Loading quiz...</div>;
  }

  // Handle the selection of an answer
  const handleAnswerSelection = (answerIndex) => {
    const updatedAnswers = [...selectedAnswers];
    updatedAnswers[currentQuestionIndex] = answerIndex;
    setSelectedAnswers(updatedAnswers);
  };

  // Handle moving to the next question
  const handleNextQuestion = () => {
    if (currentQuestionIndex < 5) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    }
  };

  // Handle previous question navigation
  const handlePreviousQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
    }
  };

  // Handle quiz submission and result
  const handleQuizSubmit = () => {
    // Calculate the score based on the selected answers
    const score = selectedAnswers.reduce((score, answer, index) => {
      if (answer !== null && answer === course.questions[index].ans) {
        score += 1;
      }
      return score;
    }, 0);

    alert(`You scored ${score}/6`);
    navigate('/');
  };

  return (
    <div className="quiz-page">
      <div className="quiz-header">
        <h1>{course.title}</h1>
        <div className="class-meta">
          <span className="class-box">Class: 7</span>
          <span className="subject-box">{course.subject}</span>
        </div>
      </div>

      <div className="quiz-content">
        <h2>Question {currentQuestionIndex + 1}</h2>
        <p>{course.questions[currentQuestionIndex].question}</p>
        <div className="options">
          {['option1', 'option2', 'option3', 'option4'].map((option, index) => (
            <button
              key={index}
              className={`option-btn ${selectedAnswers[currentQuestionIndex] === index ? 'selected' : ''}`}
              onClick={() => handleAnswerSelection(index)}
            >
              {course.questions[currentQuestionIndex][option]}
            </button>
          ))}
        </div>
      </div>

      <div className="quiz-navigation">
        <button className="prev-btn" onClick={handlePreviousQuestion} disabled={currentQuestionIndex === 0}>
          Previous
        </button>
        {currentQuestionIndex < 5 ? (
          <button className="next-btn" onClick={handleNextQuestion}>
            Next
          </button>
        ) : (
          <button className="submit-btn" onClick={handleQuizSubmit}>
            End Quiz
          </button>
        )}
      </div>
    </div>
  );
};

export default QuizPage;
