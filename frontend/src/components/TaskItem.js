import React from 'react';

/**
 * Componente de item de tarefa seguindo o princípio de responsabilidade única.
 * Responsável apenas pela exibição de uma tarefa individual.
 */
const TaskItem = ({ task, onEdit, onDelete, onToggleStatus }) => {
  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high':
        return 'bg-red-100 text-red-800';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'low':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusColor = (status) => {
    return status === 'completed' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800';
  };

  const formatDate = (dateString) => {
    if (!dateString) return '';
    return new Date(dateString).toLocaleDateString('pt-BR');
  };

  return (
    <div className={`bg-white p-4 rounded-lg shadow border-l-4 ${
      task.status === 'completed' ? 'border-green-500 opacity-75' : 'border-indigo-500'
    }`}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <h3 className={`text-lg font-semibold ${
              task.status === 'completed' ? 'line-through text-gray-500' : 'text-gray-900'
            }`}>
              {task.title}
            </h3>
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(task.priority)}`}>
              {task.priority === 'high' ? 'Alta' : task.priority === 'medium' ? 'Média' : 'Baixa'}
            </span>
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(task.status)}`}>
              {task.status === 'completed' ? 'Concluída' : 'Pendente'}
            </span>
          </div>
          
          {task.description && (
            <p className={`text-gray-600 mb-2 ${
              task.status === 'completed' ? 'line-through' : ''
            }`}>
              {task.description}
            </p>
          )}
          
          <div className="flex items-center gap-4 text-sm text-gray-500">
            <span>Criada em: {formatDate(task.created_at)}</span>
            {task.due_date && (
              <span>Vencimento: {formatDate(task.due_date)}</span>
            )}
          </div>
        </div>
        
        <div className="flex gap-2 ml-4">
          <button
            onClick={onToggleStatus}
            className={`px-3 py-1 rounded text-sm font-medium ${
              task.status === 'completed'
                ? 'bg-yellow-500 text-white hover:bg-yellow-600'
                : 'bg-green-500 text-white hover:bg-green-600'
            }`}
          >
            {task.status === 'completed' ? 'Desmarcar' : 'Concluir'}
          </button>
          
          <button
            onClick={onEdit}
            className="px-3 py-1 bg-blue-500 text-white rounded text-sm font-medium hover:bg-blue-600"
          >
            Editar
          </button>
          
          <button
            onClick={onDelete}
            className="px-3 py-1 bg-red-500 text-white rounded text-sm font-medium hover:bg-red-600"
          >
            Excluir
          </button>
        </div>
      </div>
    </div>
  );
};

export default TaskItem; 