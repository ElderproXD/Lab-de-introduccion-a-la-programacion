import sqlite3
from flask import Blueprint, render_template, request

# Creamos el Blueprint para organizar el módulo del Directorio de forma independiente
directorio_bp = Blueprint('directorio_m', __name__)

@directorio_bp.route('/directorio')
def directorio():
    # 1. Agarra lo que el usuario tecleó en la barra de búsqueda (desde la URL)
    # y borra espacios vacíos con .strip()
    busqueda = request.args.get('busqueda', '').strip()
    
    # 2. Se conecta a la base de datos y configura para leer filas como diccionarios
    conn = sqlite3.connect('hotel.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # CASO A: SI EL USUARIO ESCRIBIÓ ALGO EN LA BARRA
    if busqueda:
        # Busca por nombre, apellido o cuarto usando LIKE (búsqueda parcial)
        # El 'AND pagada = 0' es clave para que SOLO busque entre los clientes actuales del hotel
        query = """
            SELECT nombre, apellido_p, apellido_m, id_habitacion, fecha_entrada 
            FROM reservaciones 
            WHERE (nombre LIKE ? OR apellido_p LIKE ? OR id_habitacion LIKE ?) 
              AND pagada = 0
            ORDER BY id_reserva DESC
        """
        # Prepara el comodín de texto (ej: "%Cris%") para que coincida aunque no escriban el nombre completo
        termino = f"%{busqueda}%"
        
        # Le pasa el mismo término a los 3 signos de interrogación '?' (nombre, apellido, cuarto)
        cursor.execute(query, (termino, termino, termino))
        
    # CASO B: PANTALLA LIMPIA (Si la barra está vacía, muestra a todos los que están hospedados hoy)
    else:
        # Trae a absolutamente todos los huéspedes que tienen cuenta activa (pagada = 0)
        # Ordenados desde el último que llegó hasta el más antiguo (ORDER BY id_reserva DESC)
        query = """
            SELECT nombre, apellido_p, apellido_m, id_habitacion, fecha_entrada 
            FROM reservaciones 
            WHERE pagada = 0
            ORDER BY id_reserva DESC
        """
        cursor.execute(query)
        
    # 3. Descarga la lista de clientes encontrados y cierra la conexión
    lista_huespedes = cursor.fetchall()
    conn.close()
    
    # 4. Manda al HTML la lista para la tabla, y mantiene el texto en la barra para que no se borre
    return render_template('directorio.html', huespedes=lista_huespedes, busqueda=busqueda)