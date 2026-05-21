from flask import render_template

# En routes/panel_central.py
def panel_principal(datos_habitaciones): # ruta corregida 
    return render_template('PaginaPrincipal.html', habitaciones=datos_habitaciones)