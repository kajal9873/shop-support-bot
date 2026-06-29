import ChatWindow from "../components/ChatWindow";

function ChatPage() {
  return (
    <div className="chat-page">
      <header className="chat-page__header">
        <div className="chat-page__header-inner">
          <span className="chat-page__eyebrow">Apni Dukaan Ka Madadgaar</span>
          <h1>Shop Support Bot</h1>
          <p>Hindi ya English mein apna sawaal pucho — order, stock, ya timing ke baare mein.</p>
        </div>
      </header>

      <div className="chat-page__container">
        <ChatWindow />
      </div>

      <style>{`
        .chat-page {
          min-height: 100vh;
          display: flex;
          flex-direction: column;
          background: #FBF7EE;
        }
        .chat-page__header {
          background: linear-gradient(135deg, #1F2230 0%, #2D3148 100%);
          padding: 36px 24px 44px;
        }
        .chat-page__header-inner {
          max-width: 600px;
          margin: 0 auto;
        }
        .chat-page__eyebrow {
          color: #F5A623;
          font-size: 11.5px;
          font-weight: 600;
          letter-spacing: 1.2px;
          text-transform: uppercase;
        }
        .chat-page__header h1 {
          font-family: 'Poppins', sans-serif;
          margin: 8px 0 6px;
          font-size: 26px;
          color: #fff;
          font-weight: 700;
        }
        .chat-page__header p {
          margin: 0;
          font-size: 13.5px;
          color: rgba(255,255,255,0.7);
          line-height: 1.5;
        }
        .chat-page__container {
          flex: 1;
          max-width: 600px;
          width: 100%;
          margin: -28px auto 0;
          padding: 0 20px 32px;
          box-sizing: border-box;
        }
      `}</style>
    </div>
  );
}

export default ChatPage;