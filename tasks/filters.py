from django_filters import rest_framework as filters
from tasks.models import Task


class TaskFilter(filters.FilterSet):
    """
    Filtros para tarefas seguindo o princípio de responsabilidade única.
    Responsável apenas pela filtragem de tarefas.
    """
    title = filters.CharFilter(lookup_expr='icontains')
    status = filters.ChoiceFilter(choices=Task.STATUS_CHOICES)
    priority = filters.ChoiceFilter(choices=Task.PRIORITY_CHOICES)
    created_at = filters.DateTimeFromToRangeFilter()
    due_date = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Task
        fields = ['title', 'status', 'priority', 'created_at', 'due_date'] 