# 📝 To-Do List - Aplicação Full-Stack

Uma aplicação completa de gerenciamento de tarefas desenvolvida com Django REST Framework no backend e React no frontend, seguindo princípios de Clean Architecture e SOLID.

## 🏗️ Arquitetura do Projeto

### Estrutura de Diretórios
```
to-do-list/
├── backend/                 # Configurações do Django
├── accounts/               # App de autenticação
├── tasks/                  # App de gerenciamento de tarefas
├── frontend/               # Aplicação React
├── templates/              # Templates HTML
├── manage.py              # Script de gerenciamento Django
├── requirements.txt        # Dependências Python
├── start.py               # Script de inicialização
├── start.sh               # Script de inicialização (bash)
└── README.md              # Este arquivo
```

### Padrão Arquitetural
- **Backend**: Django REST Framework com arquitetura em camadas
- **Frontend**: React com Context API para gerenciamento de estado
- **Autenticação**: Token-based authentication
- **Banco de Dados**: SQLite (desenvolvimento)

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Python 3.9+
- Node.js 14+
- npm ou yarn

### 1. Clone o Repositório
```bash
git clone <url-do-repositorio>
cd to-do-list
```

### 2. Configuração do Backend

#### Instalar Dependências
```bash
pip install -r requirements.txt
```

#### Configurar Banco de Dados
```bash
python manage.py migrate
```

#### Criar Superusuário (Opcional)
```bash
python manage.py createsuperuser
```

#### Executar o Servidor Backend
```bash
python manage.py runserver
```
O backend estará disponível em: http://localhost:8000

### 3. Configuração do Frontend

#### Instalar Dependências
```bash
cd frontend
npm install
```

#### Executar o Servidor Frontend
```bash
npm start
```
O frontend estará disponível em: http://localhost:3000

### 4. Execução Automatizada
Para executar backend e frontend simultaneamente:
```bash
python start.py
```

## 📋 Funcionalidades

### Autenticação
- ✅ Registro de usuários
- ✅ Login/Logout
- ✅ Autenticação por token
- ✅ Validação de dados

### Gerenciamento de Tarefas
- ✅ Criar tarefas
- ✅ Listar tarefas do usuário
- ✅ Editar tarefas
- ✅ Excluir tarefas
- ✅ Marcar como concluída/pendente
- ✅ Filtros por status e prioridade
- ✅ Busca por título e descrição
- ✅ Ordenação por data, prioridade, status

### Interface do Usuário
- ✅ Design responsivo
- ✅ Interface moderna e intuitiva
- ✅ Feedback visual para ações
- ✅ Validação em tempo real

## 🏛️ Decisões de Design

### 1. Princípio de Responsabilidade Única (SRP)
Cada classe tem uma única responsabilidade:
- **Models**: Gerenciamento de dados
- **Serializers**: Validação e serialização
- **Views**: Lógica de negócio
- **Services**: Operações complexas

### 2. Separação de Camadas
```
┌─────────────────┐
│   Frontend      │ ← Interface do usuário
├─────────────────┤
│   API REST      │ ← Comunicação
├─────────────────┤
│   Views         │ ← Controle de requisições
├─────────────────┤
│   Serializers   │ ← Validação e formatação
├─────────────────┤
│   Models        │ ← Dados e regras de negócio
├─────────────────┤
│   Database      │ ← Persistência
└─────────────────┘
```

### 3. Autenticação Token-based
- **Vantagens**: Stateless, escalável, seguro
- **Implementação**: Django REST Framework Token Authentication
- **Segurança**: Tokens expiram com logout

### 4. Filtros e Busca
- **Django Filter**: Filtros avançados
- **Search**: Busca em múltiplos campos
- **Ordering**: Ordenação dinâmica

### 5. Isolamento de Dados
- Cada usuário vê apenas suas tarefas
- Filtros automáticos por usuário
- Validação de permissões em todas as operações

## 🔧 Configurações Técnicas

### Backend (Django)
- **Framework**: Django 5.2.4
- **API**: Django REST Framework 3.16.0
- **Autenticação**: Token Authentication
- **CORS**: django-cors-headers
- **Filtros**: django-filter
- **Banco**: SQLite (dev)

### Frontend (React)
- **Framework**: React 18
- **Roteamento**: React Router
- **Estado**: Context API
- **Formulários**: React Hook Form
- **Notificações**: React Hot Toast
- **Estilização**: Tailwind CSS

### Testes
- **Backend**: pytest + pytest-django
- **Cobertura**: pytest-cov
- **Frontend**: Jest + React Testing Library

## 📊 Estrutura de Dados

### Modelo User
```python
class User(AbstractUser):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Modelo Task
```python
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    priority = models.CharField(choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(choices=STATUS_CHOICES, default='pending')
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## 🔒 Segurança

### Implementações de Segurança
- ✅ Validação de dados em todas as entradas
- ✅ Autenticação obrigatória para operações sensíveis
- ✅ Isolamento de dados por usuário
- ✅ CORS configurado adequadamente
- ✅ Tokens de autenticação seguros
- ✅ Validação de permissões em todas as views

### Boas Práticas
- ✅ Princípio do menor privilégio
- ✅ Validação tanto no frontend quanto no backend
- ✅ Sanitização de dados
- ✅ Logs de auditoria (preparado para implementação)

## 🚀 Deploy

### Ambiente de Desenvolvimento
```bash
# Backend
python manage.py runserver

# Frontend
cd frontend && npm start
```

### Ambiente de Produção
```bash
# Configurar variáveis de ambiente
export DEBUG=False
export SECRET_KEY=sua-chave-secreta
export DATABASE_URL=sua-url-do-banco

# Coletar arquivos estáticos
python manage.py collectstatic

# Executar com gunicorn
gunicorn backend.wsgi:application
```

## 📈 Monitoramento e Logs

### Logs Configurados
- ✅ Logs de erro do Django
- ✅ Logs de requisições
- ✅ Logs de autenticação
- ✅ Logs de operações de tarefas

### Métricas Disponíveis
- ✅ Tempo de resposta das APIs
- ✅ Taxa de erro
- ✅ Uso de recursos
- ✅ Cobertura de testes

### Padrões de Código
- ✅ PEP 8 para Python
- ✅ ESLint para JavaScript
- ✅ Testes obrigatórios para novas funcionalidades
- ✅ Documentação atualizada


## 👥 Autores

- **Laís Urano** - *Desenvolvimento inicial* - [GitHub](https://github.com/uranolais)

## 🙏 Agradecimentos

- Django REST Framework pela excelente documentação
- React pela robustez do framework
- Tailwind CSS pelo design system
- Comunidade open source por todas as ferramentas utilizadas

---

**Desenvolvido com ❤️ seguindo as melhores práticas de desenvolvimento web.** 
