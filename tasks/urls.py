from django.urls import path
from tasks.views import TaskListCreateView, TaskDetailView, toggle_task_status

app_name = 'tasks'

urlpatterns = [
    path('', TaskListCreateView.as_view(), name='task-list-create'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('<int:pk>/toggle-status/', toggle_task_status, name='task-toggle-status'),
] 