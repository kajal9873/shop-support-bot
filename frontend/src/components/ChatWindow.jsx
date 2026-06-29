import { useState, useRef, useEffect } from "react";
import MessageBubble from "./MessageBubble";
import { sendMessage } from "../api/chatApi";

const QUICK_PROMPTS = ["Order status", "Shop timings", "Return policy"];

function ChatWindow() {
  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "Namaste! Aap order status, product availability ya shop timings ke baare mein pooch sakte hain.",
      timestamp: Date.now(),
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionId] = useState(() => `sess-${Date.now()}`);
  const messagesContainerRef = useRef(null);

  useEffect(() => {
    const container = messagesContainerRef.current;
    if (container) {
      container.scrollTop = container.scrollHeight;
    }
  }, [messages, loading]);

  async function handleSend(overrideText) {
    const text = (overrideText ?? input).trim();
    if (!text || loading) return;

    const userMsg = { sender: "user", text, timestamp: Date.now() };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const data = await sendMessage(text, sessionId);
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: data.reply, timestamp: Date.now() },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "Kuch gadbad ho gayi, thodi der mein try karo.",
          timestamp: Date.now(),
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  return (
    <div className="chat-window">
      <div className="chat-window__messages" ref={messagesContainerRef}>
        {messages.map((msg, idx) => (
          <MessageBubble key={idx} message={msg} />
        ))}
        {loading && (
          <div className="chat-window__typing">
            <span className="chat-window__dot" />
            <span className="chat-window__dot" />
            <span className="chat-window__dot" />
          </div>
        )}
      </div>

      {messages.length <= 1 && (
        <div className="chat-window__quick-prompts">
          {QUICK_PROMPTS.map((p) => (
            <button key={p} onClick={() => handleSend(p)} className="chat-window__chip">
              {p}
            </button>
          ))}
        </div>
      )}

      <div className="chat-window__input-row">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Apna sawaal type karo (Hindi/English)..."
          className="chat-window__input"
        />
        <button onClick={() => handleSend()} disabled={loading} className="chat-window__send-btn">
          Send
        </button>
      </div>

      <style>{`
        .chat-window {
          display: flex;
          flex-direction: column;
          height: 70vh;
          min-height: 480px;
          border-radius: 18px;
          overflow: hidden;
          background: #fff;
          box-shadow: 0 12px 32px -8px rgba(31, 34, 48, 0.18);
          border: 1px solid #EFE9DA;
        }
        .chat-window__messages {
          flex: 1;
          overflow-y: auto;
          padding: 22px 20px;
        }
        .chat-window__typing {
          display: inline-flex;
          gap: 4px;
          padding: 12px 16px;
          background: #F4F1EA;
          border-radius: 14px;
        }
        .chat-window__dot {
          width: 6px;
          height: 6px;
          border-radius: 50%;
          background: #9A9AA5;
          animation: bounce 1.2s infinite ease-in-out;
        }
        .chat-window__dot:nth-child(2) { animation-delay: 0.15s; }
        .chat-window__dot:nth-child(3) { animation-delay: 0.3s; }
        @keyframes bounce {
          0%, 80%, 100% { transform: translateY(0); opacity: 0.5; }
          40% { transform: translateY(-4px); opacity: 1; }
        }
        .chat-window__quick-prompts {
          display: flex;
          gap: 8px;
          padding: 0 16px 14px;
          flex-wrap: wrap;
        }
        .chat-window__chip {
          background: #FBF7EE;
          border: 1px solid #EFE0BE;
          color: #1F2230;
          font-size: 12.5px;
          font-weight: 500;
          padding: 7px 14px;
          border-radius: 20px;
          cursor: pointer;
          transition: all 0.15s ease;
        }
        .chat-window__chip:hover {
          background: #F5A623;
          border-color: #F5A623;
          color: #fff;
        }
        .chat-window__input-row {
          display: flex;
          gap: 10px;
          padding: 14px 16px;
          border-top: 1px solid #F0EDE4;
          background: #fff;
        }
        .chat-window__input {
          flex: 1;
          padding: 12px 16px;
          border-radius: 24px;
          border: 1.5px solid #E8E4D9;
          font-size: 14px;
          font-family: 'Inter', sans-serif;
          outline: none;
          transition: border-color 0.15s ease;
        }
        .chat-window__input:focus {
          border-color: #4F46E5;
        }
        .chat-window__send-btn {
          padding: 12px 22px;
          background: #4F46E5;
          color: #fff;
          border: none;
          border-radius: 24px;
          font-size: 13.5px;
          font-weight: 600;
          font-family: 'Inter', sans-serif;
          cursor: pointer;
          transition: background 0.15s ease;
        }
        .chat-window__send-btn:hover:not(:disabled) {
          background: #4338CA;
        }
        .chat-window__send-btn:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }
      `}</style>
    </div>
  );
}

export default ChatWindow;