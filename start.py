#!/usr/bin/env python3
"""
Script para executar frontend e backend simultaneamente
To-Do List Application
"""

import os
import sys
import time
import signal
import subprocess
import requests
from pathlib import Path

def print_status(message, status="INFO"):
    """Imprimir mensagem com formatação"""
    colors = {
        "INFO": "\033[94m",  # Azul
        "SUCCESS": "\033[92m",  # Verde
        "ERROR": "\033[91m",  # Vermelho
        "WARNING": "\033[93m",  # Amarelo
        "RESET": "\033[0m"  # Reset
    }
    print(f"{colors.get(status, '')}{message}{colors['RESET']}")

def check_port(port, service_name):
    """Verificar se uma porta está disponível"""
    try:
        response = requests.get(f"http://localhost:{port}", timeout=2)
        return True
    except:
        return False

def wait_for_service(port, service_name, max_attempts=30):
    """Aguardar até que um serviço esteja disponível"""
    print_status(f"⏳ Aguardando {service_name} na porta {port}...", "INFO")
    
    for attempt in range(max_attempts):
        if check_port(port, service_name):
            print_status(f"✅ {service_name} está rodando na porta {port}", "SUCCESS")
            return True
        time.sleep(1)
    
    print_status(f"❌ {service_name} não iniciou na porta {port}", "ERROR")
    return False

def run_command(command, cwd=None, shell=True):
    """Executar comando e retornar processo"""
    return subprocess.Popen(
        command,
        cwd=cwd,
        shell=shell,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid if os.name != 'nt' else None
    )

def kill_process(process):
    """Matar processo e seus filhos"""
    if process:
        try:
            if os.name == 'nt':
                process.terminate()
            else:
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        except:
            pass

def main():
    """Função principal"""
    print_status("🚀 Iniciando To-Do List Application...", "INFO")
    print()
    
    # Verificar se estamos no diretório correto
    if not Path("manage.py").exists():
        print_status("❌ Execute este script no diretório raiz do projeto", "ERROR")
        sys.exit(1)
    
    # Verificar ambiente virtual
    venv_path = Path("venv")
    if not venv_path.exists():
        print_status("📦 Criando ambiente virtual...", "INFO")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
    
    # Ativar ambiente virtual
    if os.name == 'nt':  # Windows
        activate_script = "venv\\Scripts\\activate"
    else:  # Linux/Mac
        activate_script = "source venv/bin/activate"
    
    # Instalar dependências do backend
    print_status("📥 Verificando dependências do backend...", "INFO")
    subprocess.run(f"{activate_script} && pip install -r requirements.txt", shell=True)
    
    # Executar migrações
    print_status("🗄️ Executando migrações...", "INFO")
    subprocess.run(f"{activate_script} && python manage.py migrate", shell=True)
    
    # Iniciar backend
    print_status("🔧 Iniciando backend Django...", "INFO")
    backend_process = run_command(
        f"{activate_script} && python manage.py runserver 0.0.0.0:8000",
        cwd="."
    )
    
    # Aguardar backend
    if not wait_for_service(8000, "Backend"):
        kill_process(backend_process)
        sys.exit(1)
    
    # Verificar se frontend existe
    frontend_path = Path("frontend")
    if not frontend_path.exists():
        print_status("❌ Diretório frontend não encontrado", "ERROR")
        kill_process(backend_process)
        sys.exit(1)
    
    # Instalar dependências do frontend se necessário
    node_modules_path = frontend_path / "node_modules"
    if not node_modules_path.exists():
        print_status("📥 Instalando dependências do frontend...", "INFO")
        subprocess.run("npm install", cwd="frontend", shell=True)
    
    # Iniciar frontend
    print_status("⚛️ Iniciando frontend React...", "INFO")
    frontend_process = run_command("npm start", cwd="frontend")
    
    # Aguardar frontend
    if not wait_for_service(3000, "Frontend"):
        kill_process(frontend_process)
        kill_process(backend_process)
        sys.exit(1)
    
    print()
    print_status("🎉 Aplicação iniciada com sucesso!", "SUCCESS")
    print_status("📱 Frontend: http://localhost:3000", "INFO")
    print_status("🔧 Backend: http://localhost:8000", "INFO")
    print_status("📚 API Docs: http://localhost:8000/api/", "INFO")
    print()
    print_status("Pressione Ctrl+C para parar ambos os servidores", "WARNING")
    
    # Função de limpeza
    def cleanup(signum, frame):
        print()
        print_status("🛑 Parando servidores...", "INFO")
        kill_process(frontend_process)
        kill_process(backend_process)
        print_status("✅ Servidores parados", "SUCCESS")
        sys.exit(0)
    
    # Capturar Ctrl+C
    signal.signal(signal.SIGINT, cleanup)
    
    # Manter script rodando
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        cleanup(None, None)

if __name__ == "__main__":
    main() 