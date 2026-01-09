import { useState } from "react";
import axios from "axios";

function ChatArea() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);

  const sendMessage = async () => {
    if (!message.trim()) return;

    const userMsg = { sender: "user", text: message };
    setChat(prev => [...prev, userMsg]);

    setMessage("");

    try {
      const res = await axios.post("http://127.0.0.1:8000/chat", {
        message: userMsg.text
      });

      const botMsg = { sender: "bot", text: res.data.reply };
      setChat(prev => [...prev, botMsg]);
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div className="chat-container">

      {chat.length === 0 && (
        <div className="welcome">
          <h1>Welcome to Smart-Study 👋</h1>
          <p>Your personal learning assistant</p>
        </div>
      )}

      <div className="chat-box">
        {chat.map((c, i) => (
          <div key={i} className={`chat-message ${c.sender}`}>
            {c.text}
          </div>
        ))}
      </div>

      <div className="input-box">
        <input
          placeholder="Ask Smart-Study..."
          value={message}
          onChange={e => setMessage(e.target.value)}
          onKeyDown={e => e.key === "Enter" && sendMessage()}
        />
        <button onClick={sendMessage}>➤</button>
      </div>

    </div>
  );
}

export default ChatArea;
