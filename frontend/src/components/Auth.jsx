import { useState } from 'react';
import api from '../api';

export default function Auth({ onLogin }) {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      if (isLogin) {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);
        
        const res = await api.post('/auth/login', formData);
        localStorage.setItem('token', res.data.access_token);
        localStorage.setItem('refresh_token', res.data.refresh_token);
        onLogin();
      } else {
        await api.post('/auth/register', { username, password });
        setIsLogin(true);
        setError('Регистрация успешна! Войдите в аккаунт.');
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Ошибка подключения к серверу');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-tabs">
        <button 
          className={isLogin ? 'active' : ''} 
          onClick={() => { setIsLogin(true); setError(''); }}>
          Вход
        </button>
        <button 
          className={!isLogin ? 'active' : ''} 
          onClick={() => { setIsLogin(false); setError(''); }}>
          Регистрация
        </button>
      </div>

      <form onSubmit={handleSubmit} className="auth-form">
        {error && <div className="alert">{error}</div>}
        
        <div className="input-group">
          <label>Логин</label>
          <input 
            type="text" 
            placeholder="Ваш логин" 
            value={username} 
            onChange={e => setUsername(e.target.value)} 
            required 
          />
        </div>

        <div className="input-group">
          <label>Пароль</label>
          <input 
            type="password" 
            placeholder="••••••••" 
            value={password} 
            onChange={e => setPassword(e.target.value)} 
            required 
          />
        </div>

        <button type="submit" className="btn-primary" disabled={loading}>
          {loading ? 'Загрузка...' : (isLogin ? 'Войти' : 'Создать аккаунт')}
        </button>
      </form>
    </div>
  );
}