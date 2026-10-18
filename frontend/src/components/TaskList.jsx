import { useState, useEffect } from 'react';
import api from '../api';

export default function TaskList() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  const fetchTasks = async () => {
    try {
      const res = await api.get('/tasks');
      setTasks(res.data);
      setError('');
    } catch (err) {
      if (err.response?.status === 401) {
        localStorage.removeItem('token');
        window.location.reload();
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchTasks(); }, []);

  const addTask = async (e) => {
    e.preventDefault();
    if (!title.trim()) return;
    try {
      await api.post('/tasks', { title });
      setTitle('');
      fetchTasks();
    } catch (err) {
      setError('Ошибка при добавлении');
    }
  };

  const toggleDone = async (position, currentDone) => {
    await api.patch(`/tasks/${position}/done`, { done: !currentDone });
    fetchTasks();
  };

  const editTask = async (position, currentTitle) => {
    const newTitle = window.prompt('Новое название:', currentTitle);
    if (newTitle && newTitle.trim() !== '' && newTitle !== currentTitle) {
      await api.put(`/tasks/${position}`, { title: newTitle });
      fetchTasks();
    }
  };

  const deleteTask = async (position) => {
    await api.delete(`/tasks/${position}`);
    fetchTasks();
  };

  return (
    <div className="tasks-container">
      <form onSubmit={addTask} className="add-task-form">
        <input 
          type="text" 
          placeholder="Что нужно сделать?" 
          value={title} 
          onChange={e => setTitle(e.target.value)} 
        />
        <button type="submit" className="btn-add">Добавить</button>
      </form>

      {error && <div className="alert">{error}</div>}

      {loading ? (
        <p className="empty-state">Загрузка...</p>
      ) : tasks.length === 0 ? (
        <p className="empty-state">Пока нет задач. Добавьте первую!</p>
      ) : (
        <ul className="task-list">
          {tasks.map(task => (
            <li key={task.id} className={`task-item ${task.done ? 'is-done' : ''}`}>
              <button 
                className="task-checkbox" 
                onClick={() => toggleDone(task.position, task.done)}>
                {task.done && (
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                )}
              </button>
              
              <span className="task-title" onClick={() => toggleDone(task.position, task.done)}>
                {task.title}
              </span>

              <div className="task-actions">
                <button className="btn-icon edit" onClick={() => editTask(task.position, task.title)} title="Редактировать">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path></svg>
                </button>
                <button className="btn-icon delete" onClick={() => deleteTask(task.position)} title="Удалить">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}