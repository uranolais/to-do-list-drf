import api from './api';

/**
 * Serviço de tarefas seguindo o princípio de responsabilidade única.
 * Responsável apenas pelas operações de CRUD de tarefas.
 */
class TaskService {
  async getTasks(params = {}) {
    try {
      const response = await api.get('/tasks/', { params });
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  }

  async getTask(id) {
    try {
      const response = await api.get(`/tasks/${id}/`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  }

  async createTask(taskData) {
    try {
      const response = await api.post('/tasks/', taskData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  }

  async updateTask(id, taskData) {
    try {
      const response = await api.put(`/tasks/${id}/`, taskData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  }

  async deleteTask(id) {
    try {
      await api.delete(`/tasks/${id}/`);
    } catch (error) {
      throw error.response?.data || error.message;
    }
  }

  async toggleTaskStatus(id) {
    try {
      const response = await api.patch(`/tasks/${id}/toggle-status/`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  }
}

export default new TaskService(); 