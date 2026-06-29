function MessageBubble({ message }) {
  const { sender, text, timestamp } = message;
  const isUser = sender === "user";

  return (
    <div className={`bubble-row ${isUser ? "bubble-row--user" : "bubble-row--bot"}`}>
      {!isUser && <div className="bubble-avatar">🛍️</div>}
      <div className={`bubble ${isUser ? "bubble--user" : "bubble--bot"}`}>
        <p className="bubble__text">{text}</p>
        {timestamp && (
          <span className="bubble__time">
            {new Date(timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
          </span>
        )}
      </div>

      <style>{`
        .bubble-row {
          display: flex;
          align-items: flex-end;
          gap: 8px;
          margin: 10px 0;
        }
        .bubble-row--user { justify-content: flex-end; }
        .bubble-row--bot { justify-content: flex-start; }
        .bubble-avatar {
          width: 28px;
          height: 28px;
          border-radius: 50%;
          background: #FBF7EE;
          border: 1px solid #EFE0BE;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 13px;
          flex-shrink: 0;
        }
        .bubble {
          max-width: 72%;
          padding: 11px 15px;
          border-radius: 16px;
          line-height: 1.45;
          font-size: 14px;
          font-family: 'Inter', sans-serif;
          word-wrap: break-word;
        }
        .bubble--user {
          background: #4F46E5;
          color: #fff;
          border-bottom-right-radius: 4px;
        }
        .bubble--bot {
          background: #F4F1EA;
          color: #1F2230;
          border-bottom-left-radius: 4px;
        }
        .bubble__text { margin: 0; }
        .bubble__time {
          display: block;
          font-size: 10px;
          opacity: 0.55;
          margin-top: 4px;
          text-align: right;
        }
      `}</style>
    </div>
  );
}

export default MessageBubble;