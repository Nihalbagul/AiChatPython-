import React, { useState } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');

  const handleSend = async () => {
    try {
      const res = await fetch('http://localhost:5000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
      });
      const data = await res.json();
      setResponse(data.response);
    } catch (error) {
      setResponse('There was an error sending the message.');
      console.error('Error:', error);
    }
  };

  return (
    <div className="App">
      <h1>Chatbot</h1>
      <input 
        type="text" 
        value={message} 
        onChange={(e) => setMessage(e.target.value)} 
        placeholder="Type your message here..."
      />
      <button onClick={handleSend}>Send</button>
      <p>Response: {response}</p>
    </div>
  );
}

export default App;
