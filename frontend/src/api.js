import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
});

// Перехватчик запросов: подставляем Access-токен
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Перехватчик ответов: если 401 — обновляем токен
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Если ошибка 401 и мы еще не пробовали обновить токен
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (!refreshToken) throw new Error('No refresh token');

        // Запрашиваем новую пару токенов
        const res = await axios.post(`${api.defaults.baseURL}/auth/refresh`, {
          refresh_token: refreshToken,
        });

        // Сохраняем новые токены
        localStorage.setItem('token', res.data.access_token);
        localStorage.setItem('refresh_token', res.data.refresh_token);

        // Повторяем оригинальный запрос с новым Access-токеном
        originalRequest.headers.Authorization = `Bearer ${res.data.access_token}`;
        return api(originalRequest);

      } catch (refreshError) {
        // Если Refresh-токен протух или неверный — разлогиниваем
        localStorage.removeItem('token');
        localStorage.removeItem('refresh_token');
        window.location.reload(); // Перезагружаем страницу, чтобы показать форму входа
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export default api;