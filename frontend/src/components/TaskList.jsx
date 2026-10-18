import { useState, useEffect } from 'react';
import api from '../api';

export default function TaskList() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState('');
  const [error, setError] = useState('');

  const fetchTasks = async () => {
    try {
      const res = await api.get('/tasks'); // Убрали слэш на конце
      setTasks(res.data);
      setError('');
    } catch (err) {
      if (err.response?.status === 401) {
        setError('Сессия истекла. Пожалуйста, перезайдите.');
        localStorage.removeItem('token');
        window.location.reload();
      }
    }
  };

  useEffect(() => { fetchTasks(); }, []);

  const addTask = async (e) => {
    e.preventDefault();
    if (!title.trim()) return;
    try {
      await api.post('/tasks', { title }); // Убрали слэш на конце
      setTitle('');
      fetchTasks();
    } catch (err) {
      setError('Ошибка при добавлении задачи');
    }
  };

  const toggleDone = async (position, currentDone) => {
    try {
      await api.patch(`/tasks/${position}/done`, { done: !currentDone });
      fetchTasks();
    } catch (err) {
      alert('Не удалось изменить статус. Попробуйте перезайти.');
    }
  };

  const editTask = async (position, currentTitle) => {
    const newTitle = window.prompt('Введите новое название задачи:', currentTitle);
    if (newTitle && newTitle.trim() !== '' && newTitle !== currentTitle) {
      try {
        await api.put(`/tasks/${position}`, { title: newTitle });
        fetchTasks();
      } catch (err) {
        alert('Не удалось отредактировать задачу.');
      }
    }
  };

  const deleteTask = async (position) => {
    try {
      await api.delete(`/tasks/${position}`);
      fetchTasks();
    } catch (err) {
      alert('Не удалось удалить задачу. Попробуйте перезайти.');
    }
  };

  return (
    <div className="task-list">
      {error && <p className="error">{error}</p>}
      
      <form onSubmit={addTask} className="add-task">
        <input 
          type="text" placeholder="Что нужно сделать?" 
          value={title} onChange={e => setTitle(e.target.value)} 
        />
        <button type="submit">Добавить</button>
      </form>

      <ul>
        {tasks.map(task => (
          <li key={task.id} className={task.done ? 'done' : ''}>
            <span onClick={() => toggleDone(task.position, task.done)} style={{ cursor: 'pointer' }}>
              {task.done ? '✅' : '⬜'} {task.title}
            </span>
            <div className="task-actions">
              <button className="edit-btn" onClick={() => editTask(task.position, task.title)}>✏️</button>
              <button className="delete-btn" onClick={() => deleteTask(task.position)}>❌</button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}