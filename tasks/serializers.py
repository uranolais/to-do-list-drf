from rest_framework import serializers
from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer para tarefas seguindo o princípio de responsabilidade única.
    Responsável apenas pela serialização de dados da tarefa.
    """
    is_completed = serializers.ReadOnlyField()

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'priority', 'status',
            'due_date', 'created_at', 'updated_at', 'is_completed'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_completed']

    def create(self, validated_data):
        """Criação de tarefa associada ao usuário atual."""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class TaskStatusSerializer(serializers.ModelSerializer):
    """
    Serializer específico para atualização de status seguindo o princípio de responsabilidade única.
    Responsável apenas pela atualização de status.
    """
    class Meta:
        model = Task
        fields = ['status'] 