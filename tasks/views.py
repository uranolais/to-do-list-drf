from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from tasks.models import Task
from tasks.serializers import TaskSerializer, TaskStatusSerializer
from tasks.filters import TaskFilter


class TaskListCreateView(generics.ListCreateAPIView):
    """
    View para listagem e criação de tarefas seguindo o princípio de responsabilidade única.
    Responsável apenas pelo CRUD básico de tarefas.
    """
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TaskFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'priority', 'status']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filtrar tarefas apenas do usuário atual."""
        return Task.objects.filter(user=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View para detalhes, atualização e exclusão de tarefas seguindo o princípio de responsabilidade única.
    Responsável apenas pelas operações em tarefas específicas.
    """
    serializer_class = TaskSerializer

    def get_queryset(self):
        """Filtrar tarefas apenas do usuário atual."""
        return Task.objects.filter(user=self.request.user)


@api_view(['PATCH'])
def toggle_task_status(request, pk):
    """
    View para alternar status da tarefa seguindo o princípio de responsabilidade única.
    Responsável apenas pela alteração de status.
    """
    try:
        task = Task.objects.get(pk=pk, user=request.user)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

    if task.status == 'completed':
        task.mark_as_pending()
    else:
        task.mark_as_completed()

    serializer = TaskSerializer(task)
    return Response(serializer.data)
