#!/bin/bash

# Script para executar frontend e backend simultaneamente
# To-Do List Application

echo "🚀 Iniciando To-Do List Application..."
echo ""

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "❌ Ambiente virtual não encontrado. Criando..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
echo "📦 Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências do backend se necessário
echo "📥 Verificando dependências do backend..."
pip install -r requirements.txt

# Executar migrações
echo "🗄️ Executando migrações..."
python manage.py migrate

# Iniciar backend em background
echo "🔧 Iniciando backend Django..."
python manage.py runserver 0.0.0.0:8000 &
BACKEND_PID=$!

# Aguardar um pouco para o backend inicializar
sleep 3

# Verificar se o backend está rodando
if curl -s http://localhost:8000/api/auth/ > /dev/null 2>&1; then
    echo "✅ Backend iniciado com sucesso em http://localhost:8000"
else
    echo "❌ Erro ao iniciar backend"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Navegar para o diretório do frontend
cd frontend

# Verificar se node_modules existe
if [ ! -d "node_modules" ]; then
    echo "📥 Instalando dependências do frontend..."
    npm install
fi

# Iniciar frontend
echo "⚛️ Iniciando frontend React..."
npm start &
FRONTEND_PID=$!

# Aguardar um pouco para o frontend inicializar
sleep 5

# Verificar se o frontend está rodando
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend iniciado com sucesso em http://localhost:3000"
else
    echo "❌ Erro ao iniciar frontend"
    kill $FRONTEND_PID 2>/dev/null
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo ""
echo "🎉 Aplicação iniciada com sucesso!"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/api/"
echo ""
echo "Pressione Ctrl+C para parar ambos os servidores"

# Função para limpar processos ao sair
cleanup() {
    echo ""
    echo "🛑 Parando servidores..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Servidores parados"
    exit 0
}

# Capturar Ctrl+C
trap cleanup SIGINT

# Manter script rodando
wait 