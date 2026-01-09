function Navbar({ isLoggedIn, onLogin, onLogout }) {
  return (
    <div className="navbar">
      <div className="logo">Smart-Study</div>

      <div className="nav-right">
        {!isLoggedIn ? (
          <button onClick={onLogin}>Login</button>
        ) : (
          <div className="profile">
            <span>👤 User</span>
            <button onClick={onLogout}>Logout</button>
          </div>
        )}
      </div>
    </div>
  );
}

export default Navbar;
