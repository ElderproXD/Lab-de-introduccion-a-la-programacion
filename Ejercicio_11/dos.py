from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "clave_secreta_2026"

USUARIO = "admin"
CONTRASENA = "admin2026"

# ==========================================
# 1. HTML PRINCIPAL (LOGIN + DASHBOARD)
# ==========================================
HTML_PRINCIPAL = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Loquendo City - Web</title>
    <style>
        body { margin: 0; font-family: 'Segoe UI', Tahoma, sans-serif; background: #f3f4f6; color: #111827; }
        .login-wrapper { display: flex; align-items: center; justify-content: center; min-height: 100vh; padding: 20px; box-sizing: border-box; }
        .card-login { background: white; padding: 40px 32px; border-radius: 14px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); width: 100%; max-width: 340px; }
        .card-login h2 { margin: 0 0 24px; text-align: center; }
        label { display: block; margin: 12px 0 6px; font-weight: bold; font-size: 14px; }
        input { width: 100%; box-sizing: border-box; padding: 12px; border: 1px solid #d1d5db; border-radius: 8px; outline: none; font-size: 16px; }
        input:focus { border-color: #2563eb; }
        .btn-ingresar { width: 100%; margin-top: 24px; padding: 12px; background: #2563eb; color: white; border: none; border-radius: 8px; font-weight: bold; font-size: 16px; cursor: pointer; }
        .btn-ingresar:hover { background: #1d4ed8; }
        .error { margin-top: 16px; color: #dc2626; text-align: center; font-size: 14px; background: #fee2e2; padding: 10px; border-radius: 6px; }
        
        .dashboard-wrapper { max-width: 1000px; margin: 0 auto; padding: 20px; }
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; background: white; padding: 15px 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
        .header h1 { margin: 0; font-size: 20px; color: #1f2937; }
        .logout-btn { text-decoration: none; color: #dc2626; font-size: 18px; background: #fee2e2; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; border-radius: 50%; font-weight: bold; }
        .cards-container { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 20px; }
        .menu-card { background: white; padding: 25px 20px; border-radius: 14px; text-decoration: none; color: inherit; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 2px solid transparent; transition: transform 0.2s; }
        .menu-card:active { transform: scale(0.98); }
        .menu-card h3 { margin: 0 0 10px 0; color: #2563eb; font-size: 18px; }
        .menu-card p { margin: 0; color: #6b7280; font-size: 14px; line-height: 1.4; }
        .icon { font-size: 32px; margin-bottom: 12px; }
    </style>
</head>
<body>
    {% if session.get("autenticado") %}
        <div class="dashboard-wrapper">
            <div class="header">
                <h1>Loquendo City 🏙️</h1>
                <a class="logout-btn" href="{{ url_for('logout') }}">✖</a>
            </div>
            <div class="cards-container">
                <a href="#" class="menu-card"><div class="icon">🔢</div><h3>1. Clasificar Número</h3><p>Par, impar, positivo o negativo.</p></a>
                <a href="#" class="menu-card"><div class="icon">🪪</div><h3>2. Categoría de Edad</h3><p>Permisos y Modo God.</p></a>
                <a href="#" class="menu-card"><div class="icon">🎟️</div><h3>3. Calcular Tarifa</h3><p>Pase Diario y descuentos.</p></a>
                
                <a href="{{ url_for('pagina_escaner') }}" class="menu-card" style="border-color: #10b981; background: #ecfdf5;">
                    <div class="icon">📱</div>
                    <h3 style="color: #10b981;">4. Escáner Móvil</h3>
                    <p>Usa la cámara de tu celular para leer códigos.</p>
                </a>
            </div>
        </div>
    {% else %}
        <div class="login-wrapper">
            <form class="card-login" method="post">
                <h2>Iniciar sesión</h2>
                <label>Usuario</label><input type="text" name="usuario" required autocomplete="off">
                <label>Contraseña</label><input type="password" name="contrasena" required>
                <button type="submit" class="btn-ingresar">Ingresar</button>
                {% if error %}<div class="error">{{ error }}</div>{% endif %}
            </form>
        </div>
    {% endif %}
</body>
</html>
"""

# ==========================================
# 2. HTML DEL ESCÁNER MÓVIL (Con JS y HD)
# ==========================================
HTML_ESCANER = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Escáner de Bolsillo</title>
    <script src="https://unpkg.com/html5-qrcode"></script>
    <style>
        body { font-family: 'Segoe UI', sans-serif; text-align: center; background: #111827; color: white; padding: 20px; margin: 0; }
        .header-escaner { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
        .btn-volver { padding: 10px 20px; background: #374151; color: white; text-decoration: none; border-radius: 8px; font-weight: bold; }
        h2 { margin: 0; font-size: 20px; color: #10b981; }
        
        /* Contenedor de la cámara expandido */
        #reader { width: 100%; max-width: 600px; margin: 0 auto; background: black; border-radius: 12px; overflow: hidden; border: 2px solid #374151 !important; }
        
        /* Resultado flotante y llamativo */
        #resultado { margin-top: 20px; font-size: 24px; color: #10b981; font-weight: bold; background: #1f2937; padding: 20px; border-radius: 12px; display: none; word-wrap: break-word; border: 2px solid #10b981; }
        
        .instrucciones { color: #9ca3af; font-size: 14px; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="header-escaner">
        <a href="{{ url_for('login') }}" class="btn-volver">⬅ Volver</a>
        <h2>📷 Escáner</h2>
    </div>
    
    <div id="reader"></div>
    <div class="instrucciones">Apunta la cámara trasera al código de barras. Asegúrate de tener buena luz w.</div>
    <div id="resultado"></div>

    <script>
        function onScanSuccess(decodedText, decodedResult) {
            // Vibra el celular si lo soporta (toque extra de pro)
            if (navigator.vibrate) { navigator.vibrate(200); }
            
            // Muestra el resultado
            let resDiv = document.getElementById('resultado');
            resDiv.style.display = "block";
            resDiv.innerHTML = "✅ ¡Código Leído!<br><br><span style='color: white; font-size: 28px;'>" + decodedText + "</span>";
            
            // Pausar el escáner para que no siga leyendo a lo loco
            html5QrcodeScanner.pause(true);
            
            // Botón para seguir escaneando
            resDiv.innerHTML += "<br><br><button onclick='reanudarEscaner()' style='padding: 10px 20px; background: #10b981; color: white; border: none; border-radius: 8px; font-weight: bold; font-size: 16px; cursor: pointer; width: 100%;'>Escanear otro</button>";
        }

        function onScanFailure(error) {
            // Ignoramos los errores mientras busca el código
        }
        
        function reanudarEscaner() {
            document.getElementById('resultado').style.display = "none";
            html5QrcodeScanner.resume();
        }

        // Configuración mamalona para celular
        let html5QrcodeScanner = new Html5QrcodeScanner(
            "reader",
            { 
                fps: 15, // Más rápido
                qrbox: { width: 280, height: 180 }, // Caja de escaneo rectangular (ideal para códigos de barras)
                aspectRatio: 1.0,
                videoConstraints: {
                    facingMode: "environment", // Fuerza la cámara trasera
                    width: { ideal: 1280 }, // Pide resolución HD
                    height: { ideal: 720 }
                }
            },
            false);
            
        html5QrcodeScanner.render(onScanSuccess, onScanFailure);
    </script>
</body>
</html>
"""

# ==========================================
# 3. RUTAS DE FLASK
# ==========================================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        contrasena = request.form.get("contrasena", "").strip()
        if usuario == USUARIO and contrasena == CONTRASENA:
            session["autenticado"] = True
            return redirect(url_for("login"))
        return render_template_string(HTML_PRINCIPAL, error="Usuario o contraseña incorrectos.")
    return render_template_string(HTML_PRINCIPAL)

@app.route("/escaner")
def pagina_escaner():
    if not session.get("autenticado"):
        return redirect(url_for("login"))
    return render_template_string(HTML_ESCANER)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    # EL SSL_CONTEXT='ADHOC' ES OBLIGATORIO PARA EL CELULAR
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context='adhoc')
