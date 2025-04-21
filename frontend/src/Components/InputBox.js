import React, { useState } from "react";
import "./InputBox.css";

function InputBox({ onSend }) {
  const [input, setInput] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onSend(input);
      setInput("");
    }
  };

  return (
    <form className="group" onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Type your message..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        className="input"
      />
      <button type="submit" className="pushable">
        <span className="shadow"></span>
        <span className="edge"></span>
        <span className="front">Send</span>
      </button>
    </form>
  );
}

export default InputBox;
