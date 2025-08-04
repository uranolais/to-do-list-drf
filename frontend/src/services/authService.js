import api from './api';

/**
 * Serviço de autenticação seguindo o princípio de responsabilidade única.
 * Responsável apenas pelas operações de autenticação.
 */
class AuthService {
  async register(userData) {
    try {
      const response = await api.post('/auth/register/', userData);
      const { token, user } = response.data;
      
      localStorage.setItem('token', token);
      localStorage.setItem('user', JSON.stringify(user));
      
      return { token, user };
    } catch (error) {
      throw error.response?.data || error.message;
    }
  }

  async login(credentials) {
    try {
      const response = await api.post('/auth/login/', credentials);
      const { token, user } = response.data;
      
      localStorage.setItem('token', token);
      localStorage.setItem('user', JSON.stringify(user));
      
      return { token, user };
    } catch (error) {
      throw error.response?.data || error.message;
    }
  }

  async logout() {
    try {
      await api.post('/auth/logout/');
    } catch (error) {
      console.error('Erro no logout:', error);
    } finally {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
    }
  }

  isAuthenticated() {
    return !!localStorage.getItem('token');
  }

  getCurrentUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  }
}

export default new AuthService(); 