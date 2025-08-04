from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from tasks.models import Task
from datetime import timedelta
import random

User = get_user_model()


class Command(BaseCommand):
    """
    Comando para criar dados de exemplo seguindo o princípio de responsabilidade única.
    Responsável apenas pela criação de dados de teste.
    """
    help = 'Cria dados de exemplo para testar a aplicação'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=5,
            help='Número de usuários para criar'
        )
        parser.add_argument(
            '--tasks-per-user',
            type=int,
            default=10,
            help='Número de tarefas por usuário'
        )

    def handle(self, *args, **options):
        self.stdout.write('🚀 Criando dados de exemplo...')
        
        # Criar usuários
        users_created = 0
        for i in range(options['users']):
            username = f'user{i+1}'
            email = f'user{i+1}@example.com'
            
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password='password123',
                    first_name=f'Usuário {i+1}',
                    last_name='Exemplo'
                )
                users_created += 1
                self.stdout.write(f'✅ Usuário criado: {username}')
        
        self.stdout.write(f'📊 {users_created} usuários criados')
        
        # Criar tarefas
        tasks_created = 0
        priorities = ['low', 'medium', 'high']
        statuses = ['pending', 'completed']
        
        task_titles = [
            'Estudar Django REST Framework',
            'Implementar autenticação',
            'Criar interface de usuário',
            'Configurar banco de dados',
            'Escrever documentação',
            'Fazer testes unitários',
            'Otimizar performance',
            'Implementar filtros',
            'Adicionar paginação',
            'Configurar CORS',
            'Criar componentes React',
            'Implementar formulários',
            'Adicionar validações',
            'Configurar rotas',
            'Implementar estado global',
            'Criar hooks customizados',
            'Adicionar notificações',
            'Implementar upload de arquivos',
            'Configurar ambiente de produção',
            'Fazer deploy da aplicação'
        ]
        
        task_descriptions = [
            'Aprender os conceitos básicos do Django REST Framework',
            'Implementar sistema de autenticação com tokens',
            'Criar interface moderna e responsiva',
            'Configurar e migrar banco de dados',
            'Documentar todas as funcionalidades',
            'Criar testes para garantir qualidade',
            'Otimizar consultas e queries',
            'Implementar sistema de filtros avançados',
            'Adicionar paginação para melhor performance',
            'Configurar CORS para comunicação frontend/backend',
            'Desenvolver componentes reutilizáveis',
            'Criar formulários com validação',
            'Adicionar validações no frontend e backend',
            'Configurar sistema de rotas',
            'Implementar gerenciamento de estado',
            'Criar hooks personalizados',
            'Adicionar sistema de notificações',
            'Implementar upload e download de arquivos',
            'Configurar ambiente de produção',
            'Fazer deploy em servidor de produção'
        ]
        
        for user in User.objects.all():
            for i in range(options['tasks_per_user']):
                title = random.choice(task_titles)
                description = random.choice(task_descriptions)
                priority = random.choice(priorities)
                status = random.choice(statuses)
                
                # Data de vencimento aleatória (entre hoje e 30 dias)
                due_date = timezone.now() + timedelta(days=random.randint(0, 30))
                
                task = Task.objects.create(
                    title=f"{title} - {user.username}",
                    description=description,
                    user=user,
                    priority=priority,
                    status=status,
                    due_date=due_date
                )
                tasks_created += 1
        
        self.stdout.write(f'📋 {tasks_created} tarefas criadas')
        self.stdout.write('✅ Dados de exemplo criados com sucesso!')
        
        # Mostrar estatísticas
        total_users = User.objects.count()
        total_tasks = Task.objects.count()
        completed_tasks = Task.objects.filter(status='completed').count()
        pending_tasks = Task.objects.filter(status='pending').count()
        
        self.stdout.write('\n📊 Estatísticas:')
        self.stdout.write(f'   👥 Usuários: {total_users}')
        self.stdout.write(f'   📋 Tarefas: {total_tasks}')
        self.stdout.write(f'   ✅ Concluídas: {completed_tasks}')
        self.stdout.write(f'   ⏳ Pendentes: {pending_tasks}')
        
        if total_tasks > 0:
            completion_rate = (completed_tasks / total_tasks) * 100
            self.stdout.write(f'   📈 Taxa de conclusão: {completion_rate:.1f}%') 