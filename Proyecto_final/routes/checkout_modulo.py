import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for

# Creamos el Blueprint para el Checkout
checkout_bp = Blueprint('checkout_m', __name__) #modulo independiente llamado checkout-m

@checkout_bp.route('/checkout', methods=['GET']) #salida de clientes y pago
def abrir_checkout():
    #  Obtiene lo que el usuario escribió en la barra de búsqueda desde la URL
    # .strip() borra los espacios de más al inicio o al final (ej: " 105 " pasa a "105")
    busqueda = request.args.get('busqueda', '').strip()
    
    # Inicializa la variable 'reserva' vacía (None) para usarla después
    reserva = None
    
# Si el usuario escribió algo en la barra de búsqueda (no está vacía)
    if busqueda:
        # Abre el archivo de la base de datos del hotel
        conn = sqlite3.connect('hotel.db')
        
        # Configura SQLite para acceder a las columnas por su nombre (ej: fila['nombre'])
        conn.row_factory = sqlite3.Row
        
        # Crea el objeto cursor para poder ejecutar comandos SQL
        cursor = conn.cursor()
        
# 1. Define la consulta SQL para buscar una reservación activa que coincida con el cuarto o el nombre
        busquedaBarra = """
            SELECT id_reserva, nombre, apellido_p, apellido_m, id_habitacion, fecha_entrada, fecha_salida, total_pagar 
            FROM reservaciones 
            WHERE (id_habitacion = ? OR nombre LIKE ?) AND pagada = 0
            LIMIT 1
        """
        # 2. Crea el comodín "%texto%" para que busque nombres que CONTENGAN lo que escribió el usuario
        termino_nombre = f"%{busqueda}%"
        
        # 3. Ejecuta la búsqueda pasando el ID exacto del cuarto o el término del nombre de forma segura
        cursor.execute(busquedaBarra, (busqueda, termino_nombre))
        
        # 4. Descarga la primera reservación encontrada (o se queda en None si no hubo coincidencias)
        reserva = cursor.fetchone()
        
        # 5. Cierra la conexión para no dejar el archivo bloqueado
        conn.close()
# Manda al usuario a la página de check-out/facturación pasándole dos datos:
    # 'reserva' (los datos del cliente encontrado o None) y 'busqueda' (lo que tecleó)
    return render_template('facturacion.html', reserva=reserva, busqueda=busqueda)

# Ruta POST para cerrar la cuenta del cliente y liberar el cuarto
@checkout_bp.route('/finalizar_estancia', methods=['POST'])
def finalizar_estancia():
    # 1. Recupera los IDs ocultos desde el formulario de facturación
    id_reserva = request.form.get('id_reserva')
    id_habitacion = request.form.get('id_habitacion')
    
    # 2. Se conecta a la base de datos
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()
    
    # 3. Marca la reservación como cobrada/pagada (cambia 0 a 1)
    cursor.execute("UPDATE reservaciones SET pagada = 1 WHERE id_reserva = ?", (id_reserva,))
    
    # 4. Libera la habitación cambiando su estatus de 'Ocupada' a 'Disponible'
    cursor.execute("UPDATE habitaciones SET estatus = 'Disponible' WHERE id = ?", (id_habitacion,))
    
    # 5. Guarda los cambios en el archivo .db y cierra la conexión
    conn.commit()
    conn.close()
    
    # 6. Redirige al recepcionista de golpe al panel principal
    return redirect(url_for('render_panel_principal'))