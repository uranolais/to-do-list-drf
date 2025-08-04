from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from tasks.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Admin customizado para o modelo Task seguindo o princípio de responsabilidade única.
    Responsável apenas pela interface de administração de tarefas.
    """
    list_display = ('title', 'user', 'priority_badge', 'status_badge', 'created_at', 'due_date', 'is_overdue')
    list_filter = ('status', 'priority', 'created_at', 'due_date', 'user')
    search_fields = ('title', 'description', 'user__username', 'user__email')
    ordering = ('-created_at',)
    actions = ['mark_as_completed', 'mark_as_pending', 'delete_selected']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('title', 'description', 'user')
        }),
        ('Status e Prioridade', {
            'fields': ('status', 'priority')
        }),
        ('Datas', {
            'fields': ('due_date', 'created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def priority_badge(self, obj):
        """Exibir prioridade como badge colorido"""
        colors = {
            'high': 'red',
            'medium': 'orange',
            'low': 'green'
        }
        color = colors.get(obj.priority, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_priority_display()
        )
    priority_badge.short_description = 'Prioridade'
    
    def status_badge(self, obj):
        """Exibir status como badge colorido"""
        color = 'green' if obj.status == 'completed' else 'blue'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def is_overdue(self, obj):
        """Verificar se a tarefa está atrasada"""
        if obj.due_date and obj.status == 'pending':
            return obj.due_date < timezone.now()
        return False
    is_overdue.boolean = True
    is_overdue.short_description = 'Atrasada'
    
    def mark_as_completed(self, request, queryset):
        """Marcar tarefas selecionadas como concluídas"""
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} tarefa(s) marcada(s) como concluída(s).')
    mark_as_completed.short_description = "Marcar como concluída"
    
    def mark_as_pending(self, request, queryset):
        """Marcar tarefas selecionadas como pendentes"""
        updated = queryset.update(status='pending')
        self.message_user(request, f'{updated} tarefa(s) marcada(s) como pendente(s).')
    mark_as_pending.short_description = "Marcar como pendente"
    
    def get_queryset(self, request):
        """Filtrar tarefas baseado nas permissões do usuário"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    
    def save_model(self, request, obj, form, change):
        """Associar tarefa ao usuário atual se não for superusuário"""
        if not change:  # Se está criando uma nova tarefa
            if not request.user.is_superuser:
                obj.user = request.user
        super().save_model(request, obj, form, change)
    
    def has_change_permission(self, request, obj=None):
        """Verificar permissão de edição"""
        if obj is None:
            return True
        return request.user.is_superuser or obj.user == request.user
    
    def has_delete_permission(self, request, obj=None):
        """Verificar permissão de exclusão"""
        if obj is None:
            return True
        return request.user.is_superuser or obj.user == request.user
    
    def has_view_permission(self, request, obj=None):
        """Verificar permissão de visualização"""
        if obj is None:
            return True
        return request.user.is_superuser or obj.user == request.user
    
    def changelist_view(self, request, extra_context=None):
        """Adicionar estatísticas à lista de tarefas"""
        extra_context = extra_context or {}
        
        # Estatísticas gerais
        if request.user.is_superuser:
            total_tasks = Task.objects.count()
            completed_tasks = Task.objects.filter(status='completed').count()
            pending_tasks = Task.objects.filter(status='pending').count()
            overdue_tasks = Task.objects.filter(
                due_date__lt=timezone.now(),
                status='pending'
            ).count()
        else:
            user_tasks = Task.objects.filter(user=request.user)
            total_tasks = user_tasks.count()
            completed_tasks = user_tasks.filter(status='completed').count()
            pending_tasks = user_tasks.filter(status='pending').count()
            overdue_tasks = user_tasks.filter(
                due_date__lt=timezone.now(),
                status='pending'
            ).count()
        
        extra_context.update({
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'overdue_tasks': overdue_tasks,
            'completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
        })
        
        return super().changelist_view(request, extra_context)
