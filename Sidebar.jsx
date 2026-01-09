function Sidebar({ isLoggedIn, onNewChat }) {
  return (
    <div className="sidebar">
      <button className="new-chat" onClick={onNewChat}>
        + New Chat
      </button>

      <h4>History</h4>
      {isLoggedIn ? (
        <ul>
          <li>Chat 1</li>
          <li>Chat 2</li>
        </ul>
      ) : (
        <p className="login-msg">Login to see history</p>
      )}
    </div>
  );
}

export default Sidebar;
