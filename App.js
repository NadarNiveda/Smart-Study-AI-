import { useState } from "react";
import Navbar from "./components/Navbar";
import Sidebar from "./components/Sidebar";
import ChatArea from "./components/ChatArea";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import "./App.css";

function App() {
  const [user, setUser] = useState(null);
  const [page, setPage] = useState("chat"); // chat | login | signup

  if (!user && page === "login") {
    return (
      <Login
        onLogin={userData => {
          setUser(userData);
          setPage("chat");
        }}
        goToSignup={() => setPage("signup")}
      />
    );
  }

  if (!user && page === "signup") {
    return <Signup goToLogin={() => setPage("login")} />;
  }

  return (
    <>
      <Navbar
        isLoggedIn={!!user}
        onLogin={() => setPage("login")}
        onLogout={() => setUser(null)}
      />

      <div className="main">
        <Sidebar
          isLoggedIn={!!user}
          onNewChat={() => window.location.reload()}
        />
        <ChatArea />
      </div>
    </>
  );
}

export default App;
