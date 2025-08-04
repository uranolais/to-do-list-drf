import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import taskService from '../services/taskService';
import toast from 'react-hot-toast';
import TaskItem from './TaskItem';
import TaskForm from './TaskForm';

/**
 * Componente de lista de tarefas seguindo o princípio de responsabilidade única.
 * Responsável apenas pela exibição e gerenciamento da lista de tarefas.
 */
const TaskList = () => {
  const { user, logout } = useAuth();
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const [filters, setFilters] = useState({
    status: '',
    priority: '',
    search: ''
  });
  const [pagination, setPagination] = useState({
    current: 1,
    total: 0,
    pageSize: 10
  });

  useEffect(() => {
    loadTasks();
  }, [filters, pagination.current]);

  const loadTasks = async () => {
    try {
      setLoading(true);
      const params = {
        page: pagination.current,
        ...filters
      };
      
      const response = await taskService.getTasks(params);
      setTasks(response.results || response);
      setPagination(prev => ({
        ...prev,
        total: response.count || response.length
      }));
    } catch (error) {
      toast.error('Erro ao carregar tarefas');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (taskData) => {
    try {
      const newTask = await taskService.createTask(taskData);
      setTasks(prev => [newTask, ...prev]);
      setShowForm(false);
      toast.success('Tarefa criada com sucesso!');
    } catch (error) {
      toast.error('Erro ao criar tarefa');
    }
  };

  const handleUpdateTask = async (id, taskData) => {
    try {
      const updatedTask = await taskService.updateTask(id, taskData);
      setTasks(prev => prev.map(task => task.id === id ? updatedTask : task));
      setEditingTask(null);
      toast.success('Tarefa atualizada com sucesso!');
    } catch (error) {
      toast.error('Erro ao atualizar tarefa');
    }
  };

  const handleDeleteTask = async (id) => {
    try {
      await taskService.deleteTask(id);
      setTasks(prev => prev.filter(task => task.id !== id));
      toast.success('Tarefa excluída com sucesso!');
    } catch (error) {
      toast.error('Erro ao excluir tarefa');
    }
  };

  const handleToggleStatus = async (id) => {
    try {
      const updatedTask = await taskService.toggleTaskStatus(id);
      setTasks(prev => prev.map(task => task.id === id ? updatedTask : task));
      toast.success('Status da tarefa alterado!');
    } catch (error) {
      toast.error('Erro ao alterar status da tarefa');
    }
  };

  const handleLogout = async () => {
    await logout();
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-lg">Carregando tarefas...</div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Minhas Tarefas</h1>
          <p className="text-gray-600">Bem-vindo, {user?.username}!</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setShowForm(true)}
            className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700"
          >
            Nova Tarefa
          </button>
          <button
            onClick={handleLogout}
            className="bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700"
          >
            Sair
          </button>
        </div>
      </div>

      {/* Filtros */}
      <div className="bg-white p-4 rounded-lg shadow mb-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <input
            type="text"
            placeholder="Buscar tarefas..."
            value={filters.search}
            onChange={(e) => setFilters(prev => ({ ...prev, search: e.target.value }))}
            className="border border-gray-300 rounded-md px-3 py-2"
          />
          <select
            value={filters.status}
            onChange={(e) => setFilters(prev => ({ ...prev, status: e.target.value }))}
            className="border border-gray-300 rounded-md px-3 py-2"
          >
            <option value="">Todos os status</option>
            <option value="pending">Pendente</option>
            <option value="completed">Concluída</option>
          </select>
          <select
            value={filters.priority}
            onChange={(e) => setFilters(prev => ({ ...prev, priority: e.target.value }))}
            className="border border-gray-300 rounded-md px-3 py-2"
          >
            <option value="">Todas as prioridades</option>
            <option value="low">Baixa</option>
            <option value="medium">Média</option>
            <option value="high">Alta</option>
          </select>
          <button
            onClick={() => setFilters({ status: '', priority: '', search: '' })}
            className="bg-gray-500 text-white px-4 py-2 rounded-md hover:bg-gray-600"
          >
            Limpar Filtros
          </button>
        </div>
      </div>

      {/* Formulário de Nova Tarefa */}
      {showForm && (
        <div className="mb-6">
          <TaskForm
            onSubmit={handleCreateTask}
            onCancel={() => setShowForm(false)}
          />
        </div>
      )}

      {/* Lista de Tarefas */}
      <div className="space-y-4">
        {tasks.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            Nenhuma tarefa encontrada.
          </div>
        ) : (
          tasks.map(task => (
            <TaskItem
              key={task.id}
              task={task}
              onEdit={() => setEditingTask(task)}
              onDelete={() => handleDeleteTask(task.id)}
              onToggleStatus={() => handleToggleStatus(task.id)}
            />
          ))
        )}
      </div>

      {/* Paginação */}
      {pagination.total > pagination.pageSize && (
        <div className="flex justify-center mt-6">
          <div className="flex gap-2">
            <button
              onClick={() => setPagination(prev => ({ ...prev, current: prev.current - 1 }))}
              disabled={pagination.current === 1}
              className="px-3 py-2 border border-gray-300 rounded-md disabled:opacity-50"
            >
              Anterior
            </button>
            <span className="px-3 py-2">
              Página {pagination.current} de {Math.ceil(pagination.total / pagination.pageSize)}
            </span>
            <button
              onClick={() => setPagination(prev => ({ ...prev, current: prev.current + 1 }))}
              disabled={pagination.current >= Math.ceil(pagination.total / pagination.pageSize)}
              className="px-3 py-2 border border-gray-300 rounded-md disabled:opacity-50"
            >
              Próxima
            </button>
          </div>
        </div>
      )}

      {/* Modal de Edição */}
      {editingTask && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <TaskForm
              task={editingTask}
              onSubmit={(data) => handleUpdateTask(editingTask.id, data)}
              onCancel={() => setEditingTask(null)}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default TaskList; 