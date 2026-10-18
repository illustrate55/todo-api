import { useState } from 'react';
import api from '../api';

export default function Auth({ onLogin }) {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      if (isLogin) {
        // Вход (OAuth2 требует form-data)
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);
        
        const res = await api.post('/auth/login', formData);
        localStorage.setItem('token', res.data.access_token);
        onLogin();
      } else {
        // Регистрация
        await api.post('/auth/register', { username, password });
        alert('Регистрация успешна! Теперь войдите.');
        setIsLogin(true);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Ошибка подключения');
    }
  };

  return (
    <div className="auth-form">
      <h2>{isLogin ? 'Вход' : 'Регистрация'}</h2>
      {error && <p className="error">{error}</p>}
      <form onSubmit={handleSubmit}>
        <input 
          type="text" placeholder="Логин" value={username} 
          onChange={e => setUsername(e.target.value)} required 
        />
        <input 
          type="password" placeholder="Пароль" value={password} 
          onChange={e => setPassword(e.target.value)} required 
        />
        <button type="submit">{isLogin ? 'Войти' : 'Создать аккаунт'}</button>
      </form>
      <p className="toggle" onClick={() => setIsLogin(!isLogin)}>
        {isLogin ? 'Нет аккаунта? Зарегистрируйтесь' : 'Уже есть аккаунт? Войдите'}
      </p>
    </div>
  );
}