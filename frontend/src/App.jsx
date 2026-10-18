import { useState, useEffect } from 'react';
import Auth from './components/Auth';
import TaskList from './components/TaskList';
import './App.css';

function App() {
  const [isAuth, setIsAuth] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) setIsAuth(true);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuth(false);
  };

  return (
    <div className="app-wrapper">
      <div className="main-card">
        <header className="app-header">
          <div className="logo">
            <span className="logo-icon">✨</span>
            <h1>Focus Board</h1>
          </div>
          {isAuth && (
            <button className="btn-logout" onClick={handleLogout} title="Выйти">
              Выйти
            </button>
          )}
        </header>
        <main className="app-content">
          {isAuth ? <TaskList /> : <Auth onLogin={() => setIsAuth(true)} />}
        </main>
      </div>
    </div>
  );
}

export default App;