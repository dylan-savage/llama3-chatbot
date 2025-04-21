import React from "react";
import "./Message.css";

function Message({ text, sender, sentiment, sentimentScores }) {
  return (
    <div className={`message ${sender}`}>
      <p>{text}</p>
      {sender === "bot" && sentiment && (
        <div className="sentiment-info">
          <small>Sentiment: {sentiment}</small>
          {sentimentScores && (
            <div className="sentiment-scores">
              {Object.entries(sentimentScores).map(([label, score]) => (
                <small key={label}>{label}: {(score * 100).toFixed(1)}%</small>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default Message;
