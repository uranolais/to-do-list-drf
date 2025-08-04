import React from 'react';
import { useForm } from 'react-hook-form';

/**
 * Componente de formulário de tarefa seguindo o princípio de responsabilidade única.
 * Responsável apenas pela interface de criação/edição de tarefas.
 */
const TaskForm = ({ task, onSubmit, onCancel }) => {
  const { register, handleSubmit, formState: { errors } } = useForm({
    defaultValues: task || {
      title: '',
      description: '',
      priority: 'medium',
      due_date: ''
    }
  });

  const handleFormSubmit = (data) => {
    // Converter a data para o formato esperado pela API
    if (data.due_date) {
      data.due_date = new Date(data.due_date).toISOString();
    }
    onSubmit(data);
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h2 className="text-xl font-semibold mb-4">
        {task ? 'Editar Tarefa' : 'Nova Tarefa'}
      </h2>
      
      <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-4">
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
            Título *
          </label>
          <input
            {...register('title', { required: 'Título é obrigatório' })}
            type="text"
            className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder="Digite o título da tarefa"
          />
          {errors.title && (
            <p className="text-red-500 text-xs mt-1">{errors.title.message}</p>
          )}
        </div>

        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
            Descrição
          </label>
          <textarea
            {...register('description')}
            rows="3"
            className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder="Digite a descrição da tarefa (opcional)"
          />
        </div>

        <div>
          <label htmlFor="priority" className="block text-sm font-medium text-gray-700 mb-1">
            Prioridade
          </label>
          <select
            {...register('priority')}
            className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="low">Baixa</option>
            <option value="medium">Média</option>
            <option value="high">Alta</option>
          </select>
        </div>

        <div>
          <label htmlFor="due_date" className="block text-sm font-medium text-gray-700 mb-1">
            Data de Vencimento
          </label>
          <input
            {...register('due_date')}
            type="datetime-local"
            className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <div className="flex gap-2 pt-4">
          <button
            type="submit"
            className="flex-1 bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            {task ? 'Atualizar' : 'Criar'} Tarefa
          </button>
          <button
            type="button"
            onClick={onCancel}
            className="flex-1 bg-gray-500 text-white py-2 px-4 rounded-md hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
          >
            Cancelar
          </button>
        </div>
      </form>
    </div>
  );
};

export default TaskForm; 