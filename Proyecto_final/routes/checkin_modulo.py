import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime

# 1. Creamos el "plano" o Blueprint. Se va a llamar 'checkin_m'
checkin_bp = Blueprint('checkin_m', __name__) #moudlo independiente usando __name__ y llaado checin_m

# 2. En lugar de @app.route, usamos @checkin_bp.route
@checkin_bp.route('/checkin') #ruta amarrada a checkin_bp
def checkin():
    # 1. Agarramos el tipo de habitación desde la URL (por defecto 'sencilla')
    tipo_habitacion = request.args.get('tipo', 'sencilla')

    conn = sqlite3.connect('hotel.db') # nuestra conexion a la base de datos 
    conn.row_factory = sqlite3.Row # para que regrese la base de datos como un diccionario
    cursor = conn.cursor() # creamos objeto para meter comandos SQL
    
    # 2. Definimos la query con el filtro doble (Tipo y Disponible)
    query_habitacion = """
        SELECT id, tipo, estatus 
        FROM habitaciones 
        WHERE tipo = ? AND estatus = 'Disponible'
    """
    
    # 3. Ejecutamos pasando la variable de forma segura en una tupla (lleva coma al final)
    cursor.execute(query_habitacion, (tipo_habitacion,))
    
    # 4. Descargamos todas las filas en la variable 'lista_habitaciones'
    lista_habitaciones = cursor.fetchall() 
    conn.close() # cierra la conexion

    # 5. Mandamos a nuestro formulario la lista filtrada
    # También te agregué 'tipo_actual' para usar en el HTML 
    return render_template('check-in.html', habitaciones=lista_habitaciones, tipo_actual=tipo_habitacion)

from flask import jsonify # <-- Asegúrate de importar jsonify arriba

@checkin_bp.route('/api/habitaciones_disponibles') #pequeñita api aqui meti algo de java jejej
def api_habitaciones():
    tipo = request.args.get('tipo', 'sencilla') #variable para guardar tipo y habitacion sencilla como predeterminada
    
    conn = sqlite3.connect('hotel.db') #conexion con base sqlite 
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    query = "SELECT id, tipo FROM habitaciones WHERE tipo = ? AND estatus = 'Disponible'" #selleciono el tipo de habtiacion y SOLO SELECCIONO LAS QUE TENGAN ESTATUS DISPONIBLE
    cursor.execute(query, (tipo,))
    filas = cursor.fetchall()
    conn.close()
    
    # Convertimos los resultados de SQLite a una lista de diccionarios común y corriente
    lista_cuartos = [{"id": f["id"], "tipo": f["tipo"]} for f in filas]
    
    # Se lo regresamos a JavaScript en formato JSON
    return jsonify(lista_cuartos) #y de aquii a el html jajaja


@checkin_bp.route('/nueva_reserva', methods=['POST']) #action /nueva_reservacion en html
def nueva_reserva(): #claseee nueva_reserva
    #request.form.get para tomar datos del formulario
    nombre = request.form.get('nombre')  #los nombres de apellido_p, telefono tiene que seer los mismos que la base de dartos
    apellido_p = request.form.get('apellido_p')
    apellido_m = request.form.get('apellido_m')
    telefono = request.form.get('telefono')
    fecha_entrada = request.form.get('fecha_entrada')
    fecha_salida = request.form.get('fecha_salida')
    id_habitacion = request.form.get('id_habitacion')

    conn = sqlite3.connect('hotel.db') #conexion a la base de datos
    cursor = conn.cursor() #conexion para poder editar la base de datos


    # Busca el precio en la base de datos usando un '?' seguro
    # El (id_habitacion,) rellena el '?' y lleva una coma al final por ser tupla
    #una tupla en python sirve para guardar datos PERO sin poder editar o borrar algo una vez creada

    cursor.execute("SELECT precio_noche FROM habitaciones WHERE id = ?", (id_habitacion,))
    # Trae un solo registro (el primero que encuentre) de la consulta SQL.
    resultado = cursor.fetchone()
    # Guarda el precio si el cuarto existe; si no, guarda 0 para que no truene
    precio_noche = resultado[0] if resultado else 0

    # Intenta convertir las fechas de texto a formato fecha real, calcula los días y el total
    try:
        # datetime.strptime: Convierte el texto "2026-05-16" en un objeto de fecha real de Python
        f_entrada = datetime.strptime(fecha_entrada, "%Y-%m-%d")
        f_salida = datetime.strptime(fecha_salida, "%Y-%m-%d")
        
        # Resta las fechas para sacar la diferencia de días exactos entre la salida y entrada
        noches = (f_salida - f_entrada).days #.days solo se usa cuando restamos o sumamos fechas
        
        # Si da 0 o negativo (error del usuario), se asegura de cobrar mínimo 1 noche
        if noches <= 0: noches = 1
        
        # Multiplica los días por el precio establecido de la base de datos SQLite
        total_pagar = noches * precio_noche

    # Si las fechas venían vacías, en formato raro o se produce cualquier error, el "except" lo atrapa
    except Exception as e:
        total_pagar = 0  # Deja el total en 0 para que el sistema no se caiga
    #insertamos es una variable de texto donde insertamos los daros
    insertar_datos = """ 
        INSERT INTO reservaciones (nombre, apellido_p, apellido_m, telefono, id_habitacion, fecha_entrada, fecha_salida, total_pagar, pagada)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
    """
    # 1. Ejecuta el INSERT (usando insertamos) para guardar al cliente en la base de datos
    cursor.execute(insertar_datos, (nombre, apellido_p, apellido_m, telefono, id_habitacion, fecha_entrada, fecha_salida, total_pagar))

    # 2. Cambia el estado del cuarto a 'Ocupada' para que nadie más lo pueda rentar
    cursor.execute("UPDATE habitaciones SET estatus = 'Ocupada' WHERE id = ?", (id_habitacion,))

    # 3. Guarda los cambios permanentemente en el archivo .db 
    conn.commit()
    # 4. Cierra la conexión para liberar la base de datos
    conn.close()

    # 5. Redirige al usuario al panel principal para que vea los cambios reflejados
    return redirect(url_for('render_panel_principal'))
