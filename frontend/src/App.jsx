import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom";
import ChatPage from "./pages/ChatPage";
import AdminPage from "./pages/AdminPage";

function App() {
  return (
    <BrowserRouter>
      <nav className="app-nav">
        <div className="app-nav__brand">
          <span className="app-nav__dot" />
          ShopSupport
        </div>
        <div className="app-nav__links">
          <NavLink to="/" end className="app-nav__link">Chat</NavLink>
          <NavLink to="/admin" className="app-nav__link">Admin</NavLink>
        </div>
      </nav>

      <Routes>
        <Route path="/" element={<ChatPage />} />
        <Route path="/admin" element={<AdminPage />} />
      </Routes>

      <style>{`
        * { box-sizing: border-box; }
        body {
          margin: 0;
          font-family: 'Inter', sans-serif;
          background: #FBF7EE;
        }
        .app-nav {
          position: sticky;
          top: 0;
          z-index: 100;
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 14px 28px;
          background: #1F2230;
        }
        .app-nav__brand {
          color: #fff;
          font-family: 'Poppins', sans-serif;
          font-weight: 700;
          font-size: 16px;
          display: flex;
          align-items: center;
          gap: 8px;
          letter-spacing: 0.2px;
        }
        .app-nav__dot {
          width: 9px;
          height: 9px;
          border-radius: 50%;
          background: #F5A623;
          display: inline-block;
        }
        .app-nav__links {
          display: flex;
          gap: 22px;
        }
        .app-nav__link {
          color: rgba(255,255,255,0.65);
          text-decoration: none;
          font-size: 13.5px;
          font-weight: 500;
          padding: 6px 4px;
          border-bottom: 2px solid transparent;
          transition: all 0.15s ease;
        }
        .app-nav__link:hover {
          color: #fff;
        }
        .app-nav__link.active {
          color: #fff;
          border-bottom-color: #F5A623;
        }
      `}</style>
    </BrowserRouter>
  );
}

export default App;