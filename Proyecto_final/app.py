import sqlite3 #para la base de datos
import os #permiso para que busque la base de datos por todos lados 
from flask import Flask, render_template, request, redirect, flash, url_for #librerias de flask que vamos a utlizar 
from routes.panel_central import panel_principal #busca la carpeta routes y se trae el archivo panel_central

# 1. Importmamos de la carpeta rutas los archvivos py
#usamos bp: blueprint es "pano de construción"
from routes.checkin_modulo import checkin_bp
from routes.directorio_modulo import directorio_bp
from routes.checkout_modulo import checkout_bp

# Buscamos la carpeta de la base de datos
base_dir = os.path.abspath(os.path.dirname(__file__)) #Averigua en qué carpeta exacta esta la base de datos.
db_path = os.path.join(base_dir, 'hotel.db') #aqui usamos os para que busque como amdinsitrador la base de datos

app = Flask(__name__)
app.secret_key = 'mi_llave_secreta_para_el_hotel'

# 2. Registramos y intregramos rutas utlizando: "app.register_blueprint"
app.register_blueprint(checkin_bp)
app.register_blueprint(directorio_bp)
app.register_blueprint(checkout_bp)

#Credenciales necesearias para pasar del login
USUARIOCORRECTO = "admin"
CONTRASENA_CORRECTA = "admin2026"

@app.route('/') #Ruta inicial que se ejeecuta primero siempre se usa @app.route con (/)
def index(): #clase index
    return render_template('index.html') #enviamos nuestra carpeta template a que corra el index.html ahi se encuentra el login

#----------------------
#LOGICAAA DEL LOGIIIN 
#----------------------
@app.route('/login', methods=['POST'])
def login():
    usuario = request.form.get("username") #agaramos los datos del html 
    password = request.form.get("password")

    if usuario == USUARIOCORRECTO and password == CONTRASENA_CORRECTA:
        return redirect("/panel") #verificamos que sean correctos y le damos acceso al panel central
    else:
        flash('Usuario o contraseña incorrectos. Intenta de nuevo.', 'error')
        # 3. Rediriges a la misma página del formulario (suponiendo que tu ruta del login es '/')
        return redirect('/')
 

#----------------
#LOGICA PANEL PRINCIPAAAAL
#--------------------
@app.route('/panel')
def render_panel_principal(): #variable conn signifa conexion
    conn = sqlite3.connect(db_path) #conectamos a la base de datos 
    conn.row_factory = sqlite3.Row #Cambia los datos de números a nombres de columna. para usar cuarto[tipo] en vez de cuarto[1]
    cursor = conn.cursor() #para ejecutar codigo sql

    cursor.execute("SELECT id, tipo, estatus FROM habitaciones") #comando sql ejecutado
    #lista_habitaciones guardamos los datos de la base de datos en esa variable para usarlos
    lista_habitaciones = cursor.fetchall() #fetchall para traer todos los datos y varibale lista_habitaciones donde se guarda
    print(f"DEBUG: Encontré {len(lista_habitaciones)} habitaciones") #verificacion rapida que si hay habitaciones
    
    conn.close() #cerramos el canal de comunicacion con la bonita base de datos
    return panel_principal(datos_habitaciones=lista_habitaciones) #guardamos la lista de habitaciones en una nueva varibale llada datos y se la pasamos al panel principal

if __name__ == '__main__': #verifcacion si se corre el archivo directo 
    app.run(debug=True) #abre el servidoooor si el programa se corrio bien