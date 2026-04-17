# 📄 **XONIAL**

**Sistema de Monitoreo de Servicio Social**

---

## ⚠️ **Advertencia**

Este código tiene únicamente **fines educativos y de gestión administrativa**. Debe utilizarse exclusivamente en instituciones educativas para el control legítimo del servicio social.

---

## 🎯 **¿Qué es XONIAL?**

XONIAL es un sistema web de gestión de servicio social para instituciones educativas. Consta de dos componentes:

- **`start.py`** - Lanzador que verifica dependencias, instala requisitos y ejecuta el programa
- **`xonial.py`** - Programa principal con toda la funcionalidad del sistema

### **El sistema permite:**
- 📊 Registrar entradas y salidas de alumnos
- 👥 Administrar información de alumnos
- ⏱️ Calcular automáticamente horas acumuladas
- 📈 Generar reportes por alumno y carrera
- 🔐 Control de acceso con autenticación segura
- 📁 Exportar datos a CSV

---

## 📥 **Instalación rápida**

```bash
git clone https://github.com/XONIDU/xonial.git
cd xonial
python start.py
```

El lanzador automáticamente:
- ✅ Detecta tu sistema operativo
- ✅ Verifica Python
- ✅ Instala Flask (con los flags correctos para tu SO)
- ✅ Crea las carpetas `templates/` y `data/`
- ✅ Ejecuta el sistema

---

## 🔧 **Instalación manual por plataforma**

### 🐧 **Arch / Manjaro**
```bash
sudo pacman -S python-pip
pip install flask --break-system-packages
python start.py
```

### 🐧 **Ubuntu / Debian**
```bash
sudo apt update
sudo apt install python3 python3-pip -y
pip3 install flask --break-system-packages
python3 start.py
```

### 🪟 **Windows**
```bash
pip install flask
python start.py
```

### 🍎 **macOS**
```bash
pip3 install flask
python3 start.py
```

---

## 🔑 **Acceso al sistema**

```
URL: http://127.0.0.1:5000/login
Usuario: xonial
Contraseña: xonial123
```

*Las credenciales pueden modificarse en `data/usuarios.csv`*

---

## 📁 **Estructura del proyecto**

```
xonial/
├── start.py          # Lanzador
├── xonial.py         # Programa principal
├── credenciales.txt  # Credenciales por defecto
├── templates/        # Plantillas HTML
└── data/             # Datos (alumnos.csv, registros.csv, usuarios.csv)
```

---

## ⚙️ **Funcionalidades principales**

- **Dashboard:** Estadísticas en tiempo real
- **Registro Rápido:** Entradas/salidas con un clic
- **Gestión de Alumnos:** CRUD completo
- **Registro Manual:** Horas históricas
- **Historial:** Seguimiento por alumno
- **Reportes:** Ranking y exportación CSV
- **Meta:** 480 horas por alumno

---

## 🎨 **Estilo visual**

Interfaz estilo **hacker/terminal**:
- 🖤 Fondo negro mate (#000000)
- 💚 Texto verde neón (#00ff9d)
- ⌨️ Tipografía monospace
- ⚡ Efectos matrix

---

## 🛑 **Detener el servidor**

`Ctrl + C` en la terminal

---

## 👨‍💻 **Créditos**

**Creador:** Darian Alberto Camacho Salas
**Frontend:** Oscar Rodolfo Barragan Perez
**Equipo:** Somos XONINDU  
**Contacto:** xonidu@gmail.com

---

**⚡ XONIAL v4.2.0 - Monitoreo de Servicio Social ⚡**
