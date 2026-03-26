from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "clave_secreta_2026"

USUARIO = "admin"
CONTRASENA = "admin2026"

LOGIN_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Loquendo City - Web</title>
    <style>
        /* Estilos generales */
        body {
            margin: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f3f4f6;
            color: #111827;
        }

        /* --- ESTILOS DEL LOGIN --- */
        .login-wrapper {
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }
        .card-login {
            background: white;
            padding: 40px 32px;
            border-radius: 14px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
            width: 340px;
        }
        .card-login h2 {
            margin: 0 0 24px;
            text-align: center;
        }
        label {
            display: block;
            margin: 12px 0 6px;
            color: #374151;
            font-weight: bold;
            font-size: 14px;
        }
        input {
            width: 100%;
            box-sizing: border-box;
            padding: 12px;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            outline: none;
            transition: border-color 0.2s;
        }
        input:focus {
            border-color: #2563eb;
        }
        .btn-ingresar {
            width: 100%;
            margin-top: 24px;
            padding: 12px;
            background: #2563eb;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            font-size: 16px;
            cursor: pointer;
            transition: background 0.2s;
        }
        .btn-ingresar:hover {
            background: #1d4ed8;
        }
        .error {
            margin-top: 16px;
            color: #dc2626;
            text-align: center;
            font-size: 14px;
            background: #fee2e2;
            padding: 10px;
            border-radius: 6px;
        }

        /* --- ESTILOS DEL DASHBOARD (MENÚ) --- */
        .dashboard-wrapper {
            max-width: 1000px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 40px;
            background: white;
            padding: 20px 30px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
        .header h1 {
            margin: 0;
            font-size: 24px;
            color: #1f2937;
        }
        .logout-btn {
            text-decoration: none;
            color: #dc2626;
            font-size: 20px;
            background: #fee2e2;
            width: 45px;
            height: 45px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            transition: all 0.3s ease;
        }
        .logout-btn:hover {
            background: #dc2626;
            color: white;
            transform: rotate(90deg);
        }
        
        /* Grid para las Cards */
        .cards-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 24px;
        }
        
        /* Estilos de cada Card individual */
        .menu-card {
            background: white;
            padding: 30px 24px;
            border-radius: 14px;
            text-decoration: none;
            color: inherit;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            border: 2px solid transparent;
            transition: all 0.3s ease;
            display: flex;
            flex-direction: column;
            align-items: flex-start;
        }
        .menu-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 12px 20px rgba(0,0,0,0.1);
            border-color: #2563eb;
        }
        .menu-card h3 {
            margin: 0 0 12px 0;
            color: #2563eb;
            font-size: 20px;
        }
        .menu-card p {
            margin: 0;
            color: #6b7280;
            line-height: 1.5;
        }
        .icon {
            font-size: 32px;
            margin-bottom: 16px;
        }
    </style>
</head>
<body>

    {% if session.get("autenticado") %}
        <div class="dashboard-wrapper">
            
            <div class="header">
                <h1>Bienvenido a Loquendo City 🏙️</h1>
                <a class="logout-btn" href="{{ url_for('logout') }}" title="Cerrar sesión">✖</a>
            </div>

            <div class="cards-container">
                
                <a href="#" class="menu-card">
                    <div class="icon">🔢</div>
                    <h3>1. Clasificar Número</h3>
                    <p>Herramienta para evaluar si un número es par, impar, positivo o negativo.</p>
                </a>

                <a href="#" class="menu-card">
                    <div class="icon">🪪</div>
                    <h3>2. Categoría de Edad</h3>
                    <p>Verificación de edad, permisos de compra, conducción y activación del Modo God.</p>
                </a>

                <a href="#" class="menu-card">
                    <div class="icon">🎟️</div>
                    <h3>3. Calcular Tarifa</h3>
                    <p>Cotizador de Pase Diario con sistema avanzado de descuentos y recargos.</p>
                </a>

            </div>
        </div>

    {% else %}
        <div class="login-wrapper">
            <form class="card-login" method="post">
                <h2>Iniciar sesión</h2>
                
                <label>Usuario</label>
                <input type="text" name="usuario" required autocomplete="off">
                
                <label>Contraseña</label>
                <input type="password" name="contrasena" required>
                
                <button type="submit" class="btn-ingresar">Ingresar</button>
                
                {% if error %}
                    <div class="error">{{ error }}</div>
                {% endif %}
            </form>
        </div>
    {% endif %}

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        contrasena = request.form.get("contrasena", "").strip()

        # En minúsculas porque en tu archivo la variable la pusiste como "admin2026"
        if usuario == USUARIO and contrasena == CONTRASENA:
            session["autenticado"] = True
            return redirect(url_for("login"))

        return render_template_string(LOGIN_HTML, error="Usuario o contraseña incorrectos.")

    return render_template_string(LOGIN_HTML, error=None)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
