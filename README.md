
# 📀 XONIAL

**Sistema de monitoreo de servicio social para instituciones educativas**  
Control de horas, reportes automáticos y gestión de alumnos.  
Desarrollado por Darian Alberto Camacho Salas – [XONIDU](https://github.com/XONIDU)

---

## 📋 Características

- ✅ **Registro rápido** – Entradas y salidas en dos clics, cálculo automático de horas  
- ✅ **Gestión completa de alumnos** – CRUD (crear, leer, actualizar, desactivar) con datos de contacto, carrera y número de cuenta  
- ✅ **Reportes en tiempo real** – Ranking de alumnos por horas acumuladas, estadísticas por carrera y progreso hacia la meta (480 horas)  
- ✅ **Registro manual** – Permite añadir horas de días anteriores o corregir errores sin perder trazabilidad  
- ✅ **Exportación a CSV** – Descarga de todos los registros o resumen de alumnos para análisis externos  
- ✅ **Autenticación segura** – Credenciales configurables (por defecto `xonial` / `xonial123`) almacenadas en CSV  
- ✅ **Interfaz estilo hacker** – Tema oscuro (negro y verde neón), tipografía monospace, diseño responsive  
- ✅ **Almacenamiento en CSV** – Sin base de datos, fácil de respaldar y editar  
- ✅ **Instalación automática de dependencias** – Detecta el sistema operativo, instala Flask y crea las carpetas necesarias (`templates/`, `data/`)  
- ✅ **Accesible desde la red local** – Comparte el sistema con cualquier dispositivo de tu WiFi/Ethernet

---

## 📦 Instalación

### Opción 1 – Clonado manual

```bash
git clone https://github.com/XONIDU/xonial.git
cd xonial
python3 start.py
```

### Opción 2 – Comando `xoninstall` (recomendado para futuras herramientas XONI)

Agrega la siguiente función a tu `~/.bashrc` con un solo comando:

```bash
echo 'xoninstall() { if [ -z "$1" ]; then echo "Uso: xoninstall <repo>"; echo "Ej: xoninstall xoniran"; else git clone "https://github.com/XONIDU/$1.git"; fi; }' >> ~/.bashrc && source ~/.bashrc && echo "✅ Listo. Usa: xoninstall xonial"
```

Luego simplemente escribe:

```bash
xoninstall xonial
cd xonial
python3 start.py
```

> **Nota:** Esta función te servirá para instalar cualquier otra herramienta futura de XONIDU (por ejemplo `xoninstall xoninas`, `xoninstall xoniran`).

---

## 🪟 Instalación en Windows

### Requisitos previos
- Tener Python 3.8+ instalado ([Descargar desde python.org](https://www.python.org/downloads/))
- Marcar **"Add Python to PATH"** durante la instalación

### Paso a paso

1. Abre **cmd** o **PowerShell** como administrador.

2. Clona o descarga el repositorio:
   ```cmd
   git clone https://github.com/XONIDU/xonial.git
   cd xonial
   ```

3. Ejecuta el lanzador:
   ```cmd
   python start.py
   ```

   O usa el **acceso directo** incluido:

   ```cmd
   XONIAL.bat
   ```

### 📄 Archivo `XONIAL.bat` (incluido en el repositorio)

```batch
@echo off
title XONIAL 2026 - Monitoreo de Servicio Social
color 0A

:: ============================================================
:: SOLICITAR PERMISOS DE ADMINISTRADOR
:: ============================================================
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Solicitando permisos de administrador...
    echo.
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B
)

:: ============================================================
:: EJECUTAR start.py CON PERMISOS DE ADMINISTRADOR
:: ============================================================
cls
echo ============================================================
echo              XONIAL 2026 - Monitoreo de Servicio Social
echo              (Modo Administrador)
echo ============================================================
echo.
echo [OK] Permisos de administrador obtenidos
echo.
echo Iniciando XONIAL...
echo.
echo [INFO] Credenciales por defecto: xonial / xonial123
echo [INFO] Accede a: http://127.0.0.1:5000/login
echo.
echo Presiona Ctrl+C para detener el servidor
echo ============================================================
echo.

python start.py

pause
```

---

## 🐧 Instalación en Linux

### Requisitos previos
- Python 3.8+ instalado (generalmente viene preinstalado)
- pip instalado

### Arch Linux / Manjaro

```bash
sudo pacman -S python-pip
git clone https://github.com/XONIDU/xonial.git
cd xonial
pip install flask --break-system-packages
python start.py
```

### Ubuntu / Debian / Linux Mint

```bash
sudo apt update
sudo apt install python3 python3-pip git -y
git clone https://github.com/XONIDU/xonial.git
cd xonial
pip3 install flask --break-system-packages
python3 start.py
```

### Fedora / RHEL / CentOS

```bash
sudo dnf install python3 python3-pip git -y
git clone https://github.com/XONIDU/xonial.git
cd xonial
pip3 install flask --break-system-packages
python3 start.py
```

### Acceso directo (Linux)

El script `start.py` crea automáticamente un archivo `INICIAR_XONIAL.sh`. Para ejecutarlo:

```bash
chmod +x INICIAR_XONIAL.sh
./INICIAR_XONIAL.sh
```

---

## 🍎 Instalación en macOS

### Requisitos previos
- Python 3.8+ instalado (recomendado via Homebrew)

### Paso a paso

```bash
# Instalar Homebrew si no lo tienes
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Python
brew install python git

# Clonar y ejecutar
git clone https://github.com/XONIDU/xonial.git
cd xonial
pip3 install flask
python3 start.py
```

### Acceso directo (macOS)

El script `start.py` crea automáticamente un archivo `INICIAR_XONIAL.command`. Haz doble clic sobre él para ejecutar el sistema.

---

## 🔧 Configuración inicial

La **primera ejecución** de `start.py` automáticamente:

1. Verifica e instala `flask` (con los flags adecuados para tu sistema operativo).  
2. Crea las carpetas `templates/` y `data/` (donde se guardarán los archivos CSV).  
3. Inicia el servidor en `http://127.0.0.1:5000`.

No requiere configuración adicional; las credenciales por defecto son:

```
Usuario: xonial
Contraseña: xonial123
```

Puedes modificarlas editando `data/usuarios.csv` o el archivo `credenciales.txt`.

---

## 🚀 Uso

### Acceso desde la red local

1. Averigua la IP de tu ordenador:  
   - **Linux/macOS:** `hostname -I`  
   - **Windows:** `ipconfig`  

2. En cualquier otro dispositivo de la misma red, abre un navegador y ve a `http://<TU-IP>:5000` (ej: `http://192.168.1.45:5000`).  

3. Introduce las credenciales (`xonial` / `xonial123`).

### Funcionalidades principales

- **Dashboard** – Muestra estadísticas en tiempo real (alumnos activos, presentes hoy, horas acumuladas).  
- **Registro rápido** – Botón que abre un modal para seleccionar alumno y tipo (entrada/salida).  
- **Gestión de alumnos** – Lista completa con opciones para editar, ver historial, activar/desactivar y agregar nuevos alumnos.  
- **Registro manual** – Formulario para agregar horas de fechas pasadas o corregir registros erróneos.  
- **Reportes** – Ranking de alumnos por horas, estadísticas por carrera y botones para exportar a CSV.

### Cierre de sesión

Usa el botón **Salir** en la barra superior; la sesión se borra completamente.

---

## 📁 Estructura del paquete

| Archivo / Directorio       | Ubicación                               |
|----------------------------|------------------------------------------|
| `xonial.py`                | Directorio de instalación (donde se clonó) |
| `start.py`                 | Mismo directorio                         |
| `templates/`               | Mismo directorio (HTML de la interfaz)   |
| `data/`                    | Mismo directorio (archivos CSV)          |
| `credenciales.txt`         | Mismo directorio (credenciales por defecto) |
| `XONIAL.bat`               | Mismo directorio (acceso directo para Windows) |

### Archivos de datos (dentro de `data/`)

- **`usuarios.csv`** – `username,password,nombre`  
- **`alumnos.csv`** – `id_alumno,nombre,carrera,semestre,num_cuenta,ocupacion,contacto,activo`  
- **`registros.csv`** – `id_registro,id_alumno,fecha,hora_entrada,hora_salida,horas_totales,observaciones,tipo_registro`

---

## 🛠️ Configuración manual (archivos CSV)

- **Cambiar credenciales** – Edita `data/usuarios.csv` y modifica la línea del usuario `xonial`.  
- **Resetear contraseña** – Si olvidaste la contraseña, elimina `data/usuarios.csv` y reinicia el sistema; se recreará con las credenciales por defecto.  
- **Cambiar meta de horas** – En `reporte_horas.html` y en la función `obtener_total_horas_alumno` puedes ajustar el valor de 480 horas.

---

## 🧪 Pruebas

Ejecuta directamente el servidor:

```bash
python3 xonial.py
```

Si todo funciona, verás mensajes en la terminal y el servidor disponible en `http://127.0.0.1:5000`.

---

## 🐛 Problemas comunes y soluciones

| Problema | Solución |
|----------|----------|
| **`flask` no instalado** | El `start.py` lo instala automáticamente. Si falla, ejecuta `pip install flask --break-system-packages` (Linux) o `pip install flask` (Windows/macOS). |
| **Puerto 5000 en uso** | Linux/macOS: `sudo fuser -k 5000/tcp` – Windows: `netstat -ano | findstr :5000` y mata el proceso. |
| **No accesible en la red** | Abre el firewall: `sudo ufw allow 5000/tcp` (Linux) o permite la aplicación en Windows Defender. |
| **Las credenciales no funcionan** | Asegúrate de usar `xonial` / `xonial123`. Si las cambiaste y olvidaste, elimina `data/usuarios.csv` y reinicia. |
| **Error al crear carpetas** | Verifica que tengas permisos de escritura en el directorio de instalación. |
| **Los reportes no se actualizan** | Revisa que los registros tengan `hora_salida` y `horas_totales` calculadas; el registro manual debe introducir ambos campos. |

---

## 📄 Licencia

© 2026 Darian Alberto Camacho Salas (XONIDU)  
Todos los derechos reservados. No se permite la copia, distribución o modificación sin autorización explícita.

---

## ✉️ Contacto

- **Creador:** Darian Alberto Camacho Salas  
- **Email:** xonidu@gmail.com  
- **GitHub:** [@XONIDU](https://github.com/XONIDU)  

---

Hecho con 🖥️ y código para simplificar la gestión del servicio social.  
**XONIAL** – Control académico sin papeleo