# 🌐 XONIAL - Monitoreo de Servicio Social
# Creador: Darian Alberto Camacho Salas
# Colaborador: Oscar Rodolfo Barragan Perez
# Equipo: XONIDU

**Sistema de control y monitoreo de servicio social**

---

## 🎯 Objetivo

XONIAL es un sistema de gestión de servicio social diseñado para instituciones educativas que permite:

- 📊 **Registrar** entradas y salidas de alumnos
- 👥 **Administrar** la información de los alumnos de servicio social
- ⏱️ **Calcular** automáticamente las horas acumuladas
- 📈 **Generar** reportes detallados por alumno y por carrera
- 🔐 **Controlar** el acceso mediante autenticación segura
- 📁 **Exportar** datos a CSV para análisis externo

---

## ⚙️ ¿Qué hace?

**Dashboard:** Vista general con estadísticas en tiempo real

**Registro Rápido:** Registro de entradas y salidas con un clic

**Gestión de Alumnos:** CRUD completo de alumnos

**Registro Manual:** Agregar horas históricas o corregir registros

**Historial:** Visualización detallada por alumno

**Reportes:** Estadísticas y ranking de horas

**Exportación:** Descarga de datos en formato CSV

### Características principales:

- ✅ Interfaz estilo terminal con tema negro y verde neón
- ✅ Cálculo automático de horas entre entrada y salida
- ✅ Sistema de login con credenciales configurables
- ✅ Persistencia de datos en archivos CSV
- ✅ Registros manuales para correcciones históricas
- ✅ Ranking de alumnos por horas acumuladas
- ✅ Exportación de reportes para Excel y análisis
- ✅ Diseño responsive para móviles y tablets

---

## 📥 Instalación

### Requisitos previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Clona el repositorio:**
```bash
git clone https://github.com/XONIDU/xonial.git
cd xonial
```

2. **Instala las dependencias:**
```bash
pip install flask
```

3. **Ejecuta el sistema:**
```bash
python start.py
```

4. **Accede al sistema:**
```
http://127.0.0.1:5000/login
```

---

## 🔑 Credenciales por defecto

```
╔══════════════════════════════════════╗
║     CREDENCIALES DE ACCESO           ║
╠══════════════════════════════════════╣
║  Usuario: xonial                     ║
║  Contraseña: xonial123               ║
╚══════════════════════════════════════╝
```

> **Nota:** Las credenciales se pueden modificar editando el archivo `data/usuarios.csv` o mediante `credenciales.txt`

---

## 📁 Estructura del proyecto

```
xonial/
├── 📄 start.py                 # Archivo principal
├── 📄 credenciales.txt         # Credenciales por defecto
├── 📁 templates/               # Plantillas HTML
│   ├── login.html              # Página de acceso
│   ├── dashboard.html          # Panel principal
│   ├── gestion_alumnos.html    # CRUD de alumnos
│   ├── editar_alumno.html      # Edición individual
│   ├── historial_alumno.html   # Historial por alumno
│   ├── registro_manual.html    # Registro manual
│   └── reporte_horas.html      # Reportes y estadísticas
└── 📁 data/                     # Datos persistentes
    ├── alumnos.csv              # Base de alumnos
    ├── registros.csv            # Registros de horas
    └── usuarios.csv             # Credenciales
```

---

## 🎨 Estilo visual

El sistema cuenta con una interfaz de estilo **hacker/terminal** con:

- 🖤 Fondo negro mate (#000000)
- 💚 Texto verde neón (#00ff9d)
- 🔲 Bordes con efecto matrix
- ⌨️ Tipografía monospace (Courier New)
- ⚡ Efectos de resplandor y animaciones
- 📊 Tablas estilo terminal con hover effects
- 🎯 Indicadores visuales para estados

---

## 🚀 Uso del sistema

### 1. Acceso al sistema
   Ingresa con las credenciales por defecto y visualiza el dashboard con estadísticas generales

### 2. Registro de entrada/salida
   Usa el botón "Registro Rápido", selecciona alumno y tipo de registro; el sistema calcula horas automáticamente

### 3. Gestión de alumnos
   Agrega nuevos alumnos con todos sus datos, edita información existente, activa o desactiva alumnos y visualiza historial individual

### 4. Reportes
   Consulta ranking de horas por alumno, estadísticas por carrera, exportación a CSV y progreso hacia la meta de 480 horas

---

## 📊 Formato de datos

### alumnos.csv
```
id_alumno,nombre,carrera,semestre,num_cuenta,ocupacion,contacto,activo
abc123,Juan Pérez,Informática,6,2023001,Apoyo Lab,5512345678,1
```

### registros.csv
```
id_registro,id_alumno,fecha,hora_entrada,hora_salida,horas_totales,observaciones,tipo_registro
def456,abc123,2024-01-15,09:00,14:00,5.0,,automatico
```

### usuarios.csv
```
username,password,nombre
xonial,xonial123,Administrador Xonial
```

---

## 🔧 Personalización

### Cambiar credenciales
1. Edita el archivo `data/usuarios.csv`
2. Modifica la línea del usuario existente
3. Reinicia el sistema

---

## 👨‍💻 Desarrollador

**Darian Alberto Camacho Salas**

---

## 📞 Contacto

¿Dudas, sugerencias o reportes de errores?

**Instagram:** @xonidu

**Facebook:** xonidu

**Email:** xonidu@gmail.com

---

## 📝 Licencia

Este proyecto está bajo una **licencia educativa**. El código puede ser utilizado con fines de aprendizaje y enseñanza, siempre respetando los derechos de autor y dando crédito al desarrollador.

**No se permite el uso comercial no autorizado ni la redistribución sin permiso explícito.**

---

### ⚡ XONIAL v1.0 - Monitoreo de Servicio Social ⚡
