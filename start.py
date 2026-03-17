#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
XONIAL 2026 - Lanzador Universal del Sistema de Monitoreo de Servicio Social
Este script verifica dependencias y ejecuta xonial.py
Desarrollado por: Darian Alberto Camacho Salas
#Somos XONINDU
"""

import subprocess
import sys
import os
import platform
import shutil
import importlib.util
import time

# Colores para terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'
    
    @staticmethod
    def supports_color():
        """Verifica si la terminal soporta colores"""
        if platform.system() == 'Windows':
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                return kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            except:
                return False
        return True

# Desactivar colores si no hay soporte
if not Colors.supports_color():
    for attr in dir(Colors):
        if not attr.startswith('_') and attr != 'supports_color':
            setattr(Colors, attr, '')

def get_system():
    """Detecta el sistema operativo"""
    return platform.system().lower()

def get_linux_distro():
    """Detecta la distribución de Linux"""
    if get_system() != 'linux':
        return None
    
    try:
        if os.path.exists('/etc/os-release'):
            with open('/etc/os-release', 'r') as f:
                content = f.read().lower()
                if 'ubuntu' in content:
                    return 'ubuntu'
                elif 'debian' in content:
                    return 'debian'
                elif 'fedora' in content:
                    return 'fedora'
                elif 'centos' in content:
                    return 'centos'
                elif 'arch' in content:
                    return 'arch'
                elif 'manjaro' in content:
                    return 'manjaro'
                elif 'mint' in content:
                    return 'mint'
        return 'linux-generico'
    except:
        return 'linux-generico'

def get_python_command():
    """Obtiene el comando Python correcto"""
    if get_system() == 'windows':
        return ['python']
    else:
        try:
            subprocess.run(['python3', '--version'], capture_output=True, check=True)
            return ['python3']
        except:
            return ['python']

def print_banner():
    """Muestra el banner de XONIAL"""
    sistema = get_system()
    distro = get_linux_distro()
    
    sistema_texto = {
        'windows': 'WINDOWS',
        'linux': f'LINUX ({distro.upper()})' if distro else 'LINUX',
        'darwin': 'MACOS'
    }.get(sistema, 'DESCONOCIDO')
    
    banner = f"""
{Colors.CYAN}{Colors.BOLD}╔═══════════════════════════════════════════════════════════╗
║                    XONIAL 2026 v1.0                          ║
║              Monitoreo de Servicio Social                     ║
║                                                               ║
║              Sistema detectado: {sistema_texto:<15}           ║
║                                                               ║
║              Desarrollado por: Darian Alberto                ║
║              Camacho Salas                                    ║
║              #Somos XONINDU                                   ║
╚═══════════════════════════════════════════════════════════╝{Colors.END}
    """
    print(banner)

def check_python():
    """Verifica Python instalado"""
    try:
        cmd = get_python_command() + ['--version']
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except:
        return False

def check_python_module(module_name):
    """Verifica si un módulo de Python está instalado"""
    return importlib.util.find_spec(module_name) is not None

def check_dependencies():
    """Verifica las dependencias de Python necesarias"""
    print(f"\n{Colors.BOLD}Verificando dependencias de Python...{Colors.END}")
    
    dependencias = [
        ('flask', 'flask', 'Framework web'),
    ]
    
    faltantes = []
    
    for modulo, paquete, desc in dependencias:
        if check_python_module(modulo):
            print(f"{Colors.GREEN}  ✓ {modulo}: OK{Colors.END}")
        else:
            print(f"{Colors.YELLOW}  ✗ {modulo}: FALTANTE{Colors.END}")
            faltantes.append(paquete)
    
    return faltantes

def install_dependencies(faltantes):
    """Instala las dependencias faltantes"""
    if not faltantes:
        return True
    
    print(f"\n{Colors.BOLD}Instalando dependencias faltantes...{Colors.END}")
    
    sistema = get_system()
    distro = get_linux_distro()
    
    if faltantes:
        print(f"Paquetes a instalar: {', '.join(faltantes)}")
        
        # Construir comando de instalación
        cmd = [sys.executable, '-m', 'pip', 'install']
        
        # Agregar opciones según sistema
        if sistema == 'linux':
            if distro in ['arch', 'manjaro', 'fedora']:
                cmd.append('--break-system-packages')
                print(f"{Colors.YELLOW}→ Usando --break-system-packages para {distro}{Colors.END}")
            else:
                # En Ubuntu/Debian más recientes también puede necesitar --break-system-packages
                try:
                    # Verificar si estamos en un sistema con external environment management
                    test_cmd = [sys.executable, '-m', 'pip', 'install', '--help']
                    result = subprocess.run(test_cmd, capture_output=True, text=True)
                    if '--break-system-packages' in result.stdout:
                        print(f"{Colors.YELLOW}→ Sistema detecta --break-system-packages disponible{Colors.END}")
                        respuesta = input("¿Usar --break-system-packages? (s/n) [recomendado para sistemas nuevos]: ")
                        if respuesta.lower() == 's':
                            cmd.append('--break-system-packages')
                        else:
                            cmd.append('--user')
                    else:
                        cmd.append('--user')
                except:
                    cmd.append('--user')
        elif sistema == 'darwin':
            cmd.append('--user')
        
        cmd.extend(faltantes)
        
        # Intentar instalación
        try:
            print(f"Ejecutando: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)
            print(f"{Colors.GREEN}✓ Dependencias instaladas correctamente{Colors.END}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"{Colors.RED}Error instalando dependencias: {e}{Colors.END}")
            print(f"\n{Colors.YELLOW}Intentando método alternativo...{Colors.END}")
            
            # Segundo intento: solo --user
            try:
                cmd2 = [sys.executable, '-m', 'pip', 'install', '--user'] + faltantes
                subprocess.run(cmd2, check=True)
                print(f"{Colors.GREEN}✓ Instaladas con --user{Colors.END}")
                return True
            except:
                print(f"{Colors.RED}✗ Falló la instalación{Colors.END}")
                print(f"\nInstala manualmente:")
                print(f"  pip install {' '.join(faltantes)}")
                return False
    
    return True

def verificar_importaciones():
    """Verifica que todas las importaciones necesarias funcionen"""
    print(f"\n{Colors.BOLD}Verificando importaciones...{Colors.END}")
    
    modulos = [
        ('flask', 'Flask'),
    ]
    
    todos_ok = True
    for modulo, nombre in modulos:
        try:
            __import__(modulo)
            print(f"{Colors.GREEN}  ✓ {nombre}: OK{Colors.END}")
        except ImportError:
            print(f"{Colors.RED}  ✗ {nombre}: FALLO{Colors.END}")
            todos_ok = False
    
    return todos_ok

def crear_estructura_directorios():
    """Crea la estructura de directorios necesaria"""
    print(f"\n{Colors.BOLD}Verificando estructura de directorios...{Colors.END}")
    
    directorios = ['templates', 'data']
    creados = []
    
    for dir_name in directorios:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            creados.append(dir_name)
            print(f"{Colors.GREEN}  ✓ Creado directorio: {dir_name}/{Colors.END}")
        else:
            print(f"{Colors.GREEN}  ✓ Directorio existe: {dir_name}/{Colors.END}")
    
    return creados

def crear_accesos_directos():
    """Crea accesos directos para cada sistema"""
    sistema = get_system()
    
    if sistema == 'windows':
        # Crear .bat para Windows
        with open('INICIAR_XONIAL.bat', 'w') as f:
            f.write("""@echo off
title XONIAL 2026 - Monitoreo de Servicio Social
color 0A
echo ========================================
echo      XONIAL 2026 - Servicio Social
echo      Desarrollado por Darian Alberto
echo      #Somos XONINDU
echo ========================================
echo.
python start.py
pause
""")
        print(f"{Colors.GREEN}✓ Creado INICIAR_XONIAL.bat - Haz doble clic para ejecutar{Colors.END}")
    
    elif sistema == 'linux':
        # Crear .sh para Linux
        with open('INICIAR_XONIAL.sh', 'w') as f:
            f.write("""#!/bin/bash
echo "========================================"
echo "      XONIAL 2026 - Servicio Social"
echo "      Desarrollado por Darian Alberto"
echo "      #Somos XONINDU"
echo "========================================"
echo ""
python3 start.py
read -p "Presiona Enter para salir"
""")
        os.chmod('INICIAR_XONIAL.sh', 0o755)
        print(f"{Colors.GREEN}✓ Creado INICIAR_XONIAL.sh - Ejecuta con: ./INICIAR_XONIAL.sh{Colors.END}")
    
    elif sistema == 'darwin':
        # Crear .command para Mac
        with open('INICIAR_XONIAL.command', 'w') as f:
            f.write("""#!/bin/bash
cd "$(dirname "$0")"
echo "========================================"
echo "      XONIAL 2026 - Servicio Social"
echo "      Desarrollado por Darian Alberto"
echo "      #Somos XONINDU"
echo "========================================"
echo ""
python3 start.py
""")
        os.chmod('INICIAR_XONIAL.command', 0o755)
        print(f"{Colors.GREEN}✓ Creado INICIAR_XONIAL.command - Haz doble clic para ejecutar{Colors.END}")

def mostrar_instrucciones():
    """Muestra instrucciones de uso"""
    instrucciones = f"""
{Colors.BOLD}📋 INSTRUCCIONES DE USO:{Colors.END}

1. Credenciales por defecto:
   {Colors.GREEN}Usuario: xonial{Colors.END}
   {Colors.GREEN}Contraseña: xonial123{Colors.END}

2. Accede al sistema:
   {Colors.CYAN}http://127.0.0.1:5000/login{Colors.END}

3. Funcionalidades principales:
   • Dashboard con estadísticas en tiempo real
   • Registro rápido de entradas y salidas
   • Gestión completa de alumnos
   • Reportes y exportación de datos

4. Para salir del servidor:
   Presiona {Colors.YELLOW}Ctrl+C{Colors.END} en esta terminal
    """
    print(instrucciones)

def verificar_xonial_py():
    """Verifica que existe xonial.py"""
    if not os.path.exists('xonial.py'):
        print(f"\n{Colors.RED}✗ Error: No se encuentra xonial.py{Colors.END}")
        print("Asegúrate de que xonial.py está en el mismo directorio")
        print("\nPuedes descargarlo desde:")
        print("  https://github.com/XONIDU/xonial")
        return False
    else:
        print(f"{Colors.GREEN}✓ Archivo xonial.py encontrado{Colors.END}")
        return True

def main():
    """Función principal"""
    # Limpiar pantalla
    if get_system() == 'windows':
        os.system('cls')
    else:
        os.system('clear')
    
    # Mostrar banner
    print_banner()
    
    # Verificar Python
    if not check_python():
        print(f"\n{Colors.RED}Error: Python no está instalado{Colors.END}")
        print("Instala Python desde: https://www.python.org/downloads/")
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
        return
    
    python_version = subprocess.run(get_python_command() + ['--version'], 
                                   capture_output=True, text=True).stdout.strip()
    print(f"{Colors.BOLD}Python:{Colors.END} {python_version}")
    print(f"{Colors.BOLD}Directorio:{Colors.END} {os.path.dirname(os.path.abspath(__file__))}")
    
    # Verificar que existe xonial.py
    if not verificar_xonial_py():
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
        return
    
    # Crear estructura de directorios
    crear_estructura_directorios()
    
    # Verificar dependencias
    faltantes = check_dependencies()
    
    if faltantes:
        print(f"\n{Colors.YELLOW}⚠ Se requiere instalar dependencias{Colors.END}")
        respuesta = input("¿Instalar automáticamente? (s/n): ")
        
        if respuesta.lower() == 's':
            if not install_dependencies(faltantes):
                print(f"\n{Colors.RED}No se pudieron instalar las dependencias{Colors.END}")
                respuesta2 = input("¿Continuar de todas formas? (s/n): ")
                if respuesta2.lower() != 's':
                    return
        else:
            print(f"\nPuedes instalarlas manualmente con:")
            print("  pip install flask")
            return
    
    # Verificar que las importaciones funcionan
    print(f"\n{Colors.BOLD}Verificando módulos...{Colors.END}")
    if not verificar_importaciones():
        print(f"\n{Colors.RED}Error: No se puede importar Flask{Colors.END}")
        print("El programa no puede continuar sin esta dependencia")
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
        return
    
    # Mostrar instrucciones
    mostrar_instrucciones()
    
    print(f"\n{Colors.BOLD}Iniciando XONIAL...{Colors.END}")
    print(f"{Colors.BOLD}Para detener el servidor:{Colors.END} Ctrl+C")
    print("-" * 60)
    
    # Pausa breve antes de iniciar
    time.sleep(2)
    
    # EJECUTAR xonial.py
    try:
        python_cmd = get_python_command()
        cmd = python_cmd + ['xonial.py']
        print(f"Ejecutando: {' '.join(cmd)}")
        print("-" * 60)
        
        # Ejecutar xonial.py
        resultado = subprocess.run(cmd)
        
        if resultado.returncode != 0:
            print(f"\n{Colors.RED}Error: xonial.py terminó con código {resultado.returncode}{Colors.END}")
            
    except FileNotFoundError:
        print(f"\n{Colors.RED}Error: No se encuentra xonial.py{Colors.END}")
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Servidor detenido por el usuario{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Error ejecutando xonial.py: {e}{Colors.END}")
    
    print(f"\n{Colors.CYAN}╔═══════════════════════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.CYAN}║{Colors.END}     Gracias por usar XONIAL 2026                          {Colors.CYAN}║{Colors.END}")
    print(f"{Colors.CYAN}║{Colors.END}     Desarrollado por: Darian Alberto Camacho Salas        {Colors.CYAN}║{Colors.END}")
    print(f"{Colors.CYAN}║{Colors.END}     #Somos XONINDU                                        {Colors.CYAN}║{Colors.END}")
    print(f"{Colors.CYAN}╚═══════════════════════════════════════════════════════════╝{Colors.END}")
    
    # Pausa al final (excepto en Windows que ya tiene pausa por el .bat)
    if get_system() != 'windows':
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")

if __name__ == '__main__':
    try:
        # Crear accesos directos
        crear_accesos_directos()
        
        # Ejecutar programa principal
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Saliendo...{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Error inesperado: {e}{Colors.END}")
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
