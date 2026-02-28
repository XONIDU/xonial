from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import csv
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.secret_key = "clave_secreta_servsocial_xonial"
app.template_folder = 'templates'

# Configuración de carpetas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FOLDER = os.path.join(BASE_DIR, 'data')
os.makedirs(CSV_FOLDER, exist_ok=True)

ALUMNOS_CSV = os.path.join(CSV_FOLDER, 'alumnos.csv')
REGISTROS_CSV = os.path.join(CSV_FOLDER, 'registros.csv')
USUARIOS_CSV = os.path.join(CSV_FOLDER, 'usuarios.csv')
CREDENCIALES_TXT = os.path.join(BASE_DIR, 'credenciales.txt')

# =============================================
# FUNCIONES AUXILIARES
# =============================================

def inicializar_csv():
    """Inicializa los archivos CSV si no existen"""
    # Usuarios con credenciales por defecto
    if not os.path.exists(USUARIOS_CSV):
        with open(USUARIOS_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['username', 'password', 'nombre'])
            writer.writerow(['xonial', 'xonial123', 'Administrador Xonial'])
    
    # Crear archivo de credenciales.txt
    if not os.path.exists(CREDENCIALES_TXT):
        with open(CREDENCIALES_TXT, 'w', encoding='utf-8') as f:
            f.write("=== CREDENCIALES POR DEFECTO ===\n")
            f.write("Usuario: xonial\n")
            f.write("Contraseña: xonial123\n")
            f.write("\n=== INSTRUCCIONES ===\n")
            f.write("1. Para cambiar credenciales, edita el archivo data/usuarios.csv\n")
            f.write("2. Mantén el formato: username,password,nombre\n")
            f.write("3. Reinicia el sistema después de los cambios\n")
    
    # Alumnos
    if not os.path.exists(ALUMNOS_CSV):
        with open(ALUMNOS_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id_alumno', 'nombre', 'carrera', 'semestre', 'num_cuenta', 'ocupacion', 'contacto', 'activo'])
    
    # Registros
    if not os.path.exists(REGISTROS_CSV):
        with open(REGISTROS_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id_registro', 'id_alumno', 'fecha', 'hora_entrada', 'hora_salida', 'horas_totales', 'observaciones', 'tipo_registro'])

def leer_csv(archivo):
    """Lee un archivo CSV y retorna lista de diccionarios"""
    if not os.path.exists(archivo):
        return []
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            return list(csv.DictReader(f))
    except Exception as e:
        print(f"Error leyendo {archivo}: {e}")
        return []

def escribir_csv(archivo, datos, campos):
    """Escribe datos en un archivo CSV"""
    try:
        with open(archivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=campos)
            writer.writeheader()
            if datos:
                writer.writerows(datos)
    except Exception as e:
        print(f"Error escribiendo {archivo}: {e}")

def generar_id_unico():
    """Genera un ID único de 8 caracteres"""
    import secrets
    import string
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))

def calcular_horas_totales(hora_entrada, hora_salida):
    """Calcula las horas entre entrada y salida"""
    try:
        entrada = datetime.strptime(hora_entrada, '%H:%M')
        salida = datetime.strptime(hora_salida, '%H:%M')
        
        # Si la salida es después de la media noche
        if salida < entrada:
            salida = salida + timedelta(days=1)
        
        diferencia = salida - entrada
        horas = diferencia.total_seconds() / 3600
        return round(horas, 2)
    except:
        return 0

def obtener_total_horas_alumno(id_alumno):
    """Calcula el total de horas acumuladas de un alumno"""
    registros = leer_csv(REGISTROS_CSV)
    total = 0
    for registro in registros:
        if registro['id_alumno'] == id_alumno and registro['horas_totales']:
            try:
                total += float(registro['horas_totales'])
            except:
                pass
    return round(total, 2)

def login_required(f):
    """Decorador para requerir autenticación"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# =============================================
# RUTAS PRINCIPALES
# =============================================

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        usuarios = leer_csv(USUARIOS_CSV)
        usuario = next((u for u in usuarios if u['username'] == username and u['password'] == password), None)
        
        if usuario:
            session['username'] = username
            session['nombre'] = usuario['nombre']
            return redirect(url_for('dashboard'))
        else:
            flash('ACCESO DENEGADO: Credenciales incorrectas')
    
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    alumnos = leer_csv(ALUMNOS_CSV)
    registros = leer_csv(REGISTROS_CSV)
    
    fecha_hoy = datetime.now().strftime('%Y-%m-%d')
    registros_hoy = [r for r in registros if r['fecha'] == fecha_hoy]
    
    alumnos_activos = len([a for a in alumnos if a.get('activo') == '1'])
    alumnos_presentes = len([r for r in registros_hoy if r.get('hora_salida') == ''])
    
    total_hoy = 0
    for r in registros_hoy:
        if r.get('hora_salida') and r.get('horas_totales'):
            try:
                total_hoy += float(r['horas_totales'])
            except:
                continue
    
    return render_template('dashboard.html', 
                         alumnos=alumnos,
                         registros_hoy=registros_hoy,
                         alumnos_activos=alumnos_activos,
                         alumnos_presentes=alumnos_presentes,
                         total_hoy=total_hoy,
                         fecha_hoy=fecha_hoy,
                         obtener_total_horas_alumno=obtener_total_horas_alumno)

@app.route('/registro-rapido', methods=['POST'])
@login_required
def registro_rapido():
    id_alumno = request.form.get('id_alumno', '')
    tipo = request.form.get('tipo', '')
    observaciones = request.form.get('observaciones', '')
    
    if not id_alumno or not tipo:
        flash('ERROR: Datos incompletos')
        return redirect(url_for('dashboard'))
    
    fecha_hoy = datetime.now().strftime('%Y-%m-%d')
    hora_actual = datetime.now().strftime('%H:%M')
    
    registros = leer_csv(REGISTROS_CSV)
    registro_hoy = next((r for r in registros if r.get('id_alumno') == id_alumno and r.get('fecha') == fecha_hoy), None)
    
    if tipo == 'entrada':
        if registro_hoy:
            flash('ALERTA: Este alumno ya tiene registro de entrada hoy')
        else:
            nuevo_registro = {
                'id_registro': generar_id_unico(),
                'id_alumno': id_alumno,
                'fecha': fecha_hoy,
                'hora_entrada': hora_actual,
                'hora_salida': '',
                'horas_totales': '',
                'observaciones': observaciones,
                'tipo_registro': 'automatico'
            }
            registros.append(nuevo_registro)
            escribir_csv(REGISTROS_CSV, registros, ['id_registro', 'id_alumno', 'fecha', 'hora_entrada', 'hora_salida', 'horas_totales', 'observaciones', 'tipo_registro'])
            flash(f'ENTRADA REGISTRADA: {hora_actual} hrs')
    
    elif tipo == 'salida':
        if not registro_hoy:
            flash('ERROR: No hay registro de entrada para hoy')
        elif registro_hoy.get('hora_salida'):
            flash('ALERTA: Ya tiene registro de salida hoy')
        else:
            horas_totales = calcular_horas_totales(registro_hoy.get('hora_entrada', ''), hora_actual)
            registro_hoy['hora_salida'] = hora_actual
            registro_hoy['horas_totales'] = str(horas_totales)
            registro_hoy['observaciones'] = observaciones if observaciones else registro_hoy.get('observaciones', '')
            
            escribir_csv(REGISTROS_CSV, registros, ['id_registro', 'id_alumno', 'fecha', 'hora_entrada', 'hora_salida', 'horas_totales', 'observaciones', 'tipo_registro'])
            flash(f'SALIDA REGISTRADA - Horas: {horas_totales:.2f}')
    
    return redirect(url_for('dashboard'))

@app.route('/gestion-alumnos')
@login_required
def gestion_alumnos():
    alumnos = leer_csv(ALUMNOS_CSV)
    return render_template('gestion_alumnos.html', 
                         alumnos=alumnos,
                         obtener_total_horas_alumno=obtener_total_horas_alumno)

@app.route('/agregar-alumno', methods=['POST'])
@login_required
def agregar_alumno():
    nombre = request.form.get('nombre', '').strip()
    carrera = request.form.get('carrera', '').strip()
    semestre = request.form.get('semestre', '').strip()
    num_cuenta = request.form.get('num_cuenta', '').strip()
    ocupacion = request.form.get('ocupacion', '').strip()
    contacto = request.form.get('contacto', '').strip()
    
    if not all([nombre, carrera, semestre, num_cuenta, ocupacion, contacto]):
        flash('ERROR: Todos los campos son obligatorios')
        return redirect(url_for('gestion_alumnos'))
    
    alumnos = leer_csv(ALUMNOS_CSV)
    
    if any(a.get('num_cuenta') == num_cuenta for a in alumnos):
        flash('ERROR: Número de cuenta ya existe')
        return redirect(url_for('gestion_alumnos'))
    
    nuevo_alumno = {
        'id_alumno': generar_id_unico(),
        'nombre': nombre,
        'carrera': carrera,
        'semestre': semestre,
        'num_cuenta': num_cuenta,
        'ocupacion': ocupacion,
        'contacto': contacto,
        'activo': '1'
    }
    
    alumnos.append(nuevo_alumno)
    escribir_csv(ALUMNOS_CSV, alumnos, ['id_alumno', 'nombre', 'carrera', 'semestre', 'num_cuenta', 'ocupacion', 'contacto', 'activo'])
    
    flash(f'ALUMNO AGREGADO: {nombre}')
    return redirect(url_for('gestion_alumnos'))

@app.route('/editar-alumno/<id_alumno>', methods=['GET', 'POST'])
@login_required
def editar_alumno(id_alumno):
    alumnos = leer_csv(ALUMNOS_CSV)
    alumno = next((a for a in alumnos if a.get('id_alumno') == id_alumno), None)
    
    if not alumno:
        flash('ERROR: Alumno no encontrado')
        return redirect(url_for('gestion_alumnos'))
    
    if request.method == 'POST':
        alumno['nombre'] = request.form.get('nombre', '').strip()
        alumno['carrera'] = request.form.get('carrera', '').strip()
        alumno['semestre'] = request.form.get('semestre', '').strip()
        alumno['num_cuenta'] = request.form.get('num_cuenta', '').strip()
        alumno['ocupacion'] = request.form.get('ocupacion', '').strip()
        alumno['contacto'] = request.form.get('contacto', '').strip()
        alumno['activo'] = request.form.get('activo', '1')
        
        escribir_csv(ALUMNOS_CSV, alumnos, ['id_alumno', 'nombre', 'carrera', 'semestre', 'num_cuenta', 'ocupacion', 'contacto', 'activo'])
        flash('DATOS ACTUALIZADOS')
        return redirect(url_for('gestion_alumnos'))
    
    return render_template('editar_alumno.html', alumno=alumno)

@app.route('/activar-alumno/<id_alumno>')
@login_required
def activar_alumno(id_alumno):
    alumnos = leer_csv(ALUMNOS_CSV)
    for alumno in alumnos:
        if alumno.get('id_alumno') == id_alumno:
            alumno['activo'] = '1'
            break
    escribir_csv(ALUMNOS_CSV, alumnos, ['id_alumno', 'nombre', 'carrera', 'semestre', 'num_cuenta', 'ocupacion', 'contacto', 'activo'])
    flash('ALUMNO ACTIVADO')
    return redirect(url_for('gestion_alumnos'))

@app.route('/desactivar-alumno/<id_alumno>')
@login_required
def desactivar_alumno(id_alumno):
    alumnos = leer_csv(ALUMNOS_CSV)
    for alumno in alumnos:
        if alumno.get('id_alumno') == id_alumno:
            alumno['activo'] = '0'
            break
    escribir_csv(ALUMNOS_CSV, alumnos, ['id_alumno', 'nombre', 'carrera', 'semestre', 'num_cuenta', 'ocupacion', 'contacto', 'activo'])
    flash('ALUMNO DESACTIVADO')
    return redirect(url_for('gestion_alumnos'))

@app.route('/historial-alumno/<id_alumno>')
@login_required
def historial_alumno(id_alumno):
    alumnos = leer_csv(ALUMNOS_CSV)
    registros = leer_csv(REGISTROS_CSV)
    
    alumno = next((a for a in alumnos if a.get('id_alumno') == id_alumno), None)
    if not alumno:
        flash('ERROR: Alumno no encontrado')
        return redirect(url_for('gestion_alumnos'))
    
    registros_alumno = [r for r in registros if r.get('id_alumno') == id_alumno]
    total_horas = obtener_total_horas_alumno(id_alumno)
    
    return render_template('historial_alumno.html', 
                         alumno=alumno, 
                         registros_alumno=registros_alumno,
                         total_horas=total_horas)

@app.route('/registro-manual')
@login_required
def registro_manual():
    alumnos = leer_csv(ALUMNOS_CSV)
    return render_template('registro_manual.html', alumnos=alumnos)

@app.route('/agregar-registro-manual', methods=['POST'])
@login_required
def agregar_registro_manual():
    id_alumno = request.form.get('id_alumno', '')
    fecha = request.form.get('fecha', '')
    hora_entrada = request.form.get('hora_entrada', '')
    hora_salida = request.form.get('hora_salida', '')
    horas_totales = request.form.get('horas_totales', '')
    observaciones = request.form.get('observaciones', '')
    
    if not all([id_alumno, fecha, hora_entrada, hora_salida]):
        flash('ERROR: Fecha y horas son obligatorias')
        return redirect(url_for('registro_manual'))
    
    if not horas_totales:
        horas_totales = calcular_horas_totales(hora_entrada, hora_salida)
    else:
        try:
            horas_totales = float(horas_totales)
        except:
            horas_totales = calcular_horas_totales(hora_entrada, hora_salida)
    
    registros = leer_csv(REGISTROS_CSV)
    
    nuevo_registro = {
        'id_registro': generar_id_unico(),
        'id_alumno': id_alumno,
        'fecha': fecha,
        'hora_entrada': hora_entrada,
        'hora_salida': hora_salida,
        'horas_totales': str(horas_totales),
        'observaciones': observaciones,
        'tipo_registro': 'manual'
    }
    
    registros.append(nuevo_registro)
    escribir_csv(REGISTROS_CSV, registros, ['id_registro', 'id_alumno', 'fecha', 'hora_entrada', 'hora_salida', 'horas_totales', 'observaciones', 'tipo_registro'])
    
    flash(f'REGISTRO MANUAL AGREGADO: {horas_totales:.2f} horas')
    return redirect(url_for('registro_manual'))

@app.route('/reporte-horas')
@login_required
def reporte_horas():
    alumnos = leer_csv(ALUMNOS_CSV)
    registros = leer_csv(REGISTROS_CSV)
    
    alumnos_con_horas = []
    for alumno in alumnos:
        if alumno.get('activo') == '1':
            total = obtener_total_horas_alumno(alumno.get('id_alumno', ''))
            alumnos_con_horas.append({
                'alumno': alumno,
                'total_horas': total
            })
    
    alumnos_con_horas.sort(key=lambda x: x['total_horas'], reverse=True)
    
    total_general = sum(a['total_horas'] for a in alumnos_con_horas)
    promedio = total_general / len(alumnos_con_horas) if alumnos_con_horas else 0
    
    fecha_actual = datetime.now()
    
    # Estadísticas por carrera
    carreras = {}
    for item in alumnos_con_horas:
        carrera = item['alumno'].get('carrera', '')
        if carrera not in carreras:
            carreras[carrera] = {'total': 0, 'alumnos': 0}
        carreras[carrera]['total'] += item['total_horas']
        carreras[carrera]['alumnos'] += 1
    
    return render_template('reporte_horas.html',
                         alumnos_con_horas=alumnos_con_horas,
                         total_general=total_general,
                         promedio=promedio,
                         fecha_actual=fecha_actual,
                         carreras=carreras)

@app.route('/exportar-csv')
@login_required
def exportar_csv():
    import io
    registros = leer_csv(REGISTROS_CSV)
    alumnos = leer_csv(ALUMNOS_CSV)
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(['Fecha', 'Alumno', 'Carrera', 'No. Cuenta', 'Entrada', 'Salida', 'Horas', 'Observaciones', 'Tipo'])
    
    for registro in registros:
        alumno = next((a for a in alumnos if a.get('id_alumno') == registro.get('id_alumno')), {})
        writer.writerow([
            registro.get('fecha', ''),
            alumno.get('nombre', ''),
            alumno.get('carrera', ''),
            alumno.get('num_cuenta', ''),
            registro.get('hora_entrada', ''),
            registro.get('hora_salida', ''),
            registro.get('horas_totales', ''),
            registro.get('observaciones', ''),
            registro.get('tipo_registro', '')
        ])
    
    from flask import make_response
    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=xonial_registros.csv'
    response.headers['Content-type'] = 'text/csv'
    return response

@app.route('/exportar-resumen')
@login_required
def exportar_resumen():
    import io
    alumnos = leer_csv(ALUMNOS_CSV)
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(['Alumno', 'Carrera', 'Semestre', 'No. Cuenta', 'Ocupación', 'Contacto', 'Horas Totales', 'Estado'])
    
    for alumno in alumnos:
        if alumno.get('activo') == '1':
            total_horas = obtener_total_horas_alumno(alumno.get('id_alumno', ''))
            writer.writerow([
                alumno.get('nombre', ''),
                alumno.get('carrera', ''),
                alumno.get('semestre', ''),
                alumno.get('num_cuenta', ''),
                alumno.get('ocupacion', ''),
                alumno.get('contacto', ''),
                f'{total_horas:.2f}',
                'Activo'
            ])
    
    from flask import make_response
    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=xonial_resumen.csv'
    response.headers['Content-type'] = 'text/csv'
    return response

@app.route('/logout')
def logout():
    session.clear()
    flash('SESIÓN TERMINADA')
    return redirect(url_for('login'))

if __name__ == '__main__':
    inicializar_csv()
    print("""
    ╔══════════════════════════════════════╗
    ║     XONIAL - Sistema de Monitoreo    ║
    ║       Servicio Social v1.0           ║
    ╚══════════════════════════════════════╝
    
    Backend: Darian Alberto Camacho Salas
    Fronted: Oscar Rodolfo Barragan Perez
    Asesor: Dr. Raul Dali Cruz Morales

    [*] Sistema inicializado correctamente
    [*] Credenciales por defecto:
        └─ Usuario: xonial
        └─ Contraseña: xonial123
    [*] Archivo de credenciales: credenciales.txt
    [*] Servidor corriendo en: http://127.0.0.1:5115
    """)
    app.run(debug=True, host='0.0.0.0', port=5115)
