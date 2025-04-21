import React, { useState } from "react";
import Message from "./Message";
import InputBox from "./InputBox";
import "./Chatbox.css";

function Chatbox() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async (userMessage) => {
    console.log("Sending message:", userMessage);
    const userMsgObj = { text: userMessage, sender: "user" };
    setMessages(prevMessages => [...prevMessages, userMsgObj]);
    setIsLoading(true);

    try {
      console.log("Making fetch request...");
      const response = await fetch('http://localhost:5050/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({ message: userMessage })
      });

      console.log("Response received:", response);
      console.log("Response status:", response.status);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log("Parsed response data:", data);
      
      const botMsgObj = { 
        text: data.response || "Sorry, I received an empty response.", 
        sender: "bot",
        sentiment: data.sentiment,
        sentimentScores: data.sentiment_scores
      };
      setMessages(prevMessages => [...prevMessages, botMsgObj]);
      
    } catch (error) {
      console.error('Error details:', error);
      const errorMsgObj = { 
        text: "Sorry, I'm having trouble connecting to the server.", 
        sender: "bot" 
      };
      setMessages(prevMessages => [...prevMessages, errorMsgObj]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chatbox">
      <div className="messages">
        {messages.map((msg, index) => (
          <Message 
            key={index} 
            text={msg.text} 
            sender={msg.sender}
            sentiment={msg.sentiment}
            sentimentScores={msg.sentimentScores}
          />
        ))}
        {isLoading && <div className="loading">Bot is typing...</div>}
      </div>
      <InputBox onSend={handleSend} />
    </div>
  );
}

export default Chatbox;
