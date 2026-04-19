#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
XONIAL - Lanzador Universal
Sistema de Monitoreo de Servicio Social

Desarrollado por: Darian Alberto Camacho Salas
Organización: XONIDU
"""

import subprocess
import sys
import os
import time
import platform
import shutil
import importlib.util
import webbrowser

# ============================================================================
# Colores para terminal
# ============================================================================
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'
    
    @staticmethod
    def supports_color():
        if platform.system() == 'Windows':
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                return kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            except:
                return False
        return True

if not Colors.supports_color():
    for attr in dir(Colors):
        if not attr.startswith('_') and attr != 'supports_color':
            setattr(Colors, attr, '')

# ============================================================================
# Detección del sistema
# ============================================================================
def get_system():
    return platform.system().lower()

def get_linux_distro():
    if get_system() != 'linux':
        return None
    try:
        if os.path.exists('/etc/os-release'):
            with open('/etc/os-release', 'r') as f:
                content = f.read().lower()
                if 'ubuntu' in content or 'debian' in content or 'mint' in content:
                    return 'debian-based'
                elif 'arch' in content or 'manjaro' in content:
                    return 'arch-based'
                elif 'fedora' in content:
                    return 'fedora'
                elif 'centos' in content or 'rhel' in content:
                    return 'centos'
        if shutil.which('apt'):
            return 'debian-based'
        elif shutil.which('pacman'):
            return 'arch-based'
        elif shutil.which('dnf'):
            return 'fedora'
        elif shutil.which('yum'):
            return 'centos'
        return 'linux-generico'
    except:
        return 'linux-generico'

def get_python_command():
    if get_system() == 'windows':
        return ['python']
    else:
        try:
            subprocess.run(['python3', '--version'], capture_output=True, check=True)
            return ['python3']
        except:
            return ['python']

def get_pip_command():
    return [sys.executable, '-m', 'pip']

def get_install_flags():
    flags = []
    sistema = get_system()
    distro = get_linux_distro()
    if sistema == 'linux':
        if distro in ['arch-based', 'fedora']:
            flags.append('--break-system-packages')
        else:
            flags.append('--user')
    elif sistema == 'darwin':
        flags.append('--user')
    return flags

def print_banner():
    sistema = get_system()
    distro = get_linux_distro()
    sistema_texto = {
        'windows': 'WINDOWS',
        'linux': f'LINUX ({distro.upper()})' if distro else 'LINUX',
        'darwin': 'MACOS'
    }.get(sistema, 'DESCONOCIDO')
    
    banner = f"""
{Colors.PURPLE}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗
║                     XONIAL 2026 v1.0                         ║
║              Monitoreo de Servicio Social                     ║
║                                                            ║
║               Sistema detectado: {sistema_texto:<27} ║
║                                                            ║
║               Desarrollado por: Darian Alberto             ║
║                      Camacho Salas                         ║
║                      Organización: XONIDU                  ║
╚══════════════════════════════════════════════════════════════╝{Colors.END}
    """
    print(banner)

# ============================================================================
# Verificación e instalación de pip
# ============================================================================
def check_python():
    try:
        cmd = get_python_command() + ['--version']
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except:
        return False

def check_pip():
    try:
        cmd = get_pip_command() + ['--version']
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except:
        return False

def install_pip_linux():
    distro = get_linux_distro()
    print(f"{Colors.YELLOW}Instalando pip en Linux ({distro})...{Colors.END}")
    if distro == 'debian-based':
        try:
            subprocess.run(['sudo', 'apt', 'update'], check=False)
            subprocess.run(['sudo', 'apt', 'install', '-y', 'python3-pip'], check=True)
            return True
        except:
            return False
    elif distro == 'arch-based':
        try:
            subprocess.run(['sudo', 'pacman', '-S', '--noconfirm', 'python-pip'], check=True)
            return True
        except:
            return False
    elif distro == 'fedora':
        try:
            subprocess.run(['sudo', 'dnf', 'install', '-y', 'python3-pip'], check=True)
            return True
        except:
            return False
    elif distro == 'centos':
        try:
            subprocess.run(['sudo', 'yum', 'install', '-y', 'python3-pip'], check=True)
            return True
        except:
            return False
    return False

def install_pip_windows():
    print(f"{Colors.YELLOW}Instalando pip en Windows...{Colors.END}")
    try:
        subprocess.run([sys.executable, '-m', 'ensurepip', '--upgrade'], check=True)
        return True
    except:
        try:
            import urllib.request
            urllib.request.urlretrieve('https://bootstrap.pypa.io/get-pip.py', 'get-pip.py')
            subprocess.run([sys.executable, 'get-pip.py'], check=True)
            os.remove('get-pip.py')
            return True
        except:
            return False

# ============================================================================
# Dependencias de Python (solo Flask)
# ============================================================================
REQUISITOS = ['flask']

def check_dependencies():
    print(f"\n{Colors.BOLD}📦 Verificando dependencias...{Colors.END}")
    missing = []
    for req in REQUISITOS:
        try:
            __import__(req)
            print(f"{Colors.GREEN}  ✓ {req} ya instalado{Colors.END}")
        except ImportError:
            print(f"{Colors.YELLOW}  ✗ {req} (faltante){Colors.END}")
            missing.append(req)
    return missing

def install_dependencies(missing):
    if not missing:
        return True
    print(f"\n{Colors.BOLD}Instalando dependencias faltantes...{Colors.END}")
    pip_cmd = get_pip_command()
    flags = get_install_flags()
    success = True
    for req in missing:
        try:
            cmd = pip_cmd + ['install', req] + flags
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"{Colors.GREEN}    ✓ {req}{Colors.END}")
        except:
            try:
                cmd2 = pip_cmd + ['install', req]
                subprocess.run(cmd2, check=True)
                print(f"{Colors.GREEN}    ✓ {req} (sin flags){Colors.END}")
            except:
                print(f"{Colors.RED}    ✗ {req}{Colors.END}")
                success = False
    return success

# ============================================================================
# Estructura de directorios
# ============================================================================
def crear_estructura():
    """Crea las carpetas necesarias: templates y data"""
    print(f"\n{Colors.BOLD}📁 Verificando estructura de directorios...{Colors.END}")
    for d in ['templates', 'data']:
        if not os.path.exists(d):
            os.makedirs(d)
            print(f"{Colors.GREEN}  ✓ Creado: {d}/{Colors.END}")
        else:
            print(f"{Colors.GREEN}  ✓ Ya existe: {d}/{Colors.END}")

# ============================================================================
# Ejecución principal
# ============================================================================
def main():
    # Limpiar pantalla
    os.system('clear' if get_system() != 'windows' else 'cls')
    print_banner()
    
    sistema = get_system()
    distro = get_linux_distro()
    print(f"{Colors.BOLD}Sistema operativo:{Colors.END} {sistema}")
    if distro:
        print(f"{Colors.BOLD}Distribución:{Colors.END} {distro}")
    print(f"{Colors.BOLD}Python:{Colors.END} {sys.version.split()[0]}")
    print(f"{Colors.BOLD}Directorio:{Colors.END} {os.getcwd()}")
    
    # Verificar existencia de xonial.py
    if not os.path.exists('xonial.py'):
        print(f"\n{Colors.RED}❌ Error: No se encuentra xonial.py{Colors.END}")
        print("Asegúrate de que el archivo xonial.py esté en este directorio.")
        input("\nPresiona Enter para salir...")
        sys.exit(1)
    
    # Verificar Python
    if not check_python():
        print(f"\n{Colors.RED}❌ Python no está instalado{Colors.END}")
        print("Instala Python desde https://www.python.org/downloads/")
        input("\nPresiona Enter para salir...")
        sys.exit(1)
    
    # Verificar pip
    if not check_pip():
        print(f"\n{Colors.YELLOW}⚠️ Pip no encontrado. Instalando...{Colors.END}")
        if sistema == 'linux':
            if not install_pip_linux():
                print(f"{Colors.RED}No se pudo instalar pip. Instálalo manualmente.{Colors.END}")
                input("\nPresiona Enter para salir...")
                sys.exit(1)
        elif sistema == 'windows':
            if not install_pip_windows():
                print(f"{Colors.RED}No se pudo instalar pip. Ejecuta como administrador.{Colors.END}")
                input("\nPresiona Enter para salir...")
                sys.exit(1)
        else:
            print(f"{Colors.YELLOW}Instala pip manualmente y vuelve a ejecutar.{Colors.END}")
            input("\nPresiona Enter para salir...")
            sys.exit(1)
    
    # Dependencias
    missing = check_dependencies()
    if missing:
        print(f"\n{Colors.YELLOW}Faltan {len(missing)} dependencias.{Colors.END}")
        resp = input("¿Instalar automáticamente? (s/n): ")
        if resp.lower() == 's':
            if not install_dependencies(missing):
                print(f"{Colors.YELLOW}Continuando a pesar de errores...{Colors.END}")
        else:
            print(f"{Colors.YELLOW}No se instalarán. El programa podría fallar.{Colors.END}")
    
    # Crear estructura de directorios
    crear_estructura()
    
    # Mensaje de inicio
    print(f"\n{Colors.BOLD}🚀 Iniciando XONIAL...{Colors.END}")
    print(f"{Colors.CYAN}📌 El servidor estará disponible en: http://127.0.0.1:5000{Colors.END}")
    print(f"{Colors.CYAN}📌 Credenciales por defecto: xonial / xonial123{Colors.END}")
    print(f"{Colors.YELLOW}▶️  Presiona Ctrl+C para detener el servidor{Colors.END}")
    print("-" * 60)
    
    # Ejecutar xonial.py
    try:
        python_cmd = get_python_command()
        cmd = python_cmd + ['xonial.py']
        # Abrir navegador después de un breve retraso
        def abrir_navegador():
            time.sleep(2)
            webbrowser.open('http://127.0.0.1:5000')
        threading.Thread(target=abrir_navegador, daemon=True).start()
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}🛑 Servidor detenido por el usuario{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error al ejecutar xonial.py: {e}{Colors.END}")
    
    print(f"\n{Colors.PURPLE}╔══════════════════════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.PURPLE}║{Colors.END}     Gracias por usar XONIAL 2026                          {Colors.PURPLE}║{Colors.END}")
    print(f"{Colors.PURPLE}║{Colors.END}     Desarrollado por: Darian Alberto Camacho Salas        {Colors.PURPLE}║{Colors.END}")
    print(f"{Colors.PURPLE}║{Colors.END}     #Somos XONIDU                                         {Colors.PURPLE}║{Colors.END}")
    print(f"{Colors.PURPLE}╚══════════════════════════════════════════════════════════╝{Colors.END}")
    
    if get_system() != 'windows':
        input("\nPresiona Enter para salir...")

if __name__ == '__main__':
    import threading
    main()
