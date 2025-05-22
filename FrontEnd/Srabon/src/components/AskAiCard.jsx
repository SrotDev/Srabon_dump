import React from 'react';
import { useNavigate } from 'react-router-dom';

const AskAiCard = () => {
  const navigate = useNavigate();

  return (
    <div className="ask-ai-card" onClick={() => navigate('/chat')}>
      <div className="ask-ai-content">
        <h3>🧠 Ask your doubts to AI</h3>
        <p>Our intelligent assistant is ready to help you understand tough topics, answer tricky questions, or even summarize lessons for you.</p>
        <button className="ask-btn">Go to Chat</button>
      </div>
    </div>
  );
};

export default AskAiCard;
