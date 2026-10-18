import { useState, useEffect } from 'react';
import Auth from './components/Auth';
import TaskList from './components/TaskList';
import api from './api'; // <-- Импортируем api
import './App.css';

function App() {
  const [isAuth, setIsAuth] = useState(false);
  const [username, setUsername] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuth(true);
      // Запрашиваем данные о пользователе
      api.get('/users/me')
        .then(res => setUsername(res.data.username))
        .catch(() => handleLogout()); // Если токен протух — разлогиниваем
    }
  }, []);

  const handleLogin = () => {
    setIsAuth(true);
    api.get('/users/me').then(res => setUsername(res.data.username));
  };

    const handleLogout = async () => {
    try {
      await api.post('/auth/logout'); // Сообщаем бэкенду
    } catch (e) {
      console.error("Logout error", e);
    } finally {
      localStorage.removeItem('token');
      localStorage.removeItem('refresh_token'); // <-- Удаляем и refresh
      setIsAuth(false);
      setUsername('');
    }
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
            <div className="user-info">
              <span className="username">Привет, <b>{username}</b>!</span>
              <button className="btn-logout" onClick={handleLogout} title="Выйти">
                Выйти
              </button>
            </div>
          )}
        </header>
        <main className="app-content">
          {isAuth ? <TaskList /> : <Auth onLogin={handleLogin} />}
        </main>
      </div>
    </div>
  );
}

export default App;