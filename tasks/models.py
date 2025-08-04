from django.db import models
from django.conf import settings


class Task(models.Model):
    """
    Modelo de tarefa seguindo o princípio de responsabilidade única.
    Responsável apenas por gerenciar informações da tarefa.
    """
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tasks'
        ordering = ['-created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return self.title

    @property
    def is_completed(self):
        """Propriedade para verificar se a tarefa está concluída."""
        return self.status == 'completed'

    def mark_as_completed(self):
        """Método para marcar tarefa como concluída."""
        self.status = 'completed'
        self.save(update_fields=['status', 'updated_at'])

    def mark_as_pending(self):
        """Método para marcar tarefa como pendente."""
        self.status = 'pending'
        self.save(update_fields=['status', 'updated_at'])

