import { useState, useEffect } from 'react';
import Auth from './components/Auth';
import TaskList from './components/TaskList';
import './App.css';

function App() {
  const [isAuth, setIsAuth] = useState(false);

  useEffect(() => {
    // Если в localStorage есть токен, считаем, что юзер залогинен
    const token = localStorage.getItem('token');
    if (token) setIsAuth(true);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuth(false);
  };

  return (
    <div className="container">
      <header>
        <h1>Мои Задачи</h1>
        {isAuth && <button className="logout-btn" onClick={handleLogout}>Выйти</button>}
      </header>
      <main>
        {isAuth ? <TaskList /> : <Auth onLogin={() => setIsAuth(true)} />}
      </main>
    </div>
  );
}

export default App;