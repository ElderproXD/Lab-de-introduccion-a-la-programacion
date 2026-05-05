from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)
app.secret_key = "clave_secreta_2026"

# ==========================================
# BASE DE DATOS Y MEMORIA DEL SERVIDOR
# ==========================================
# Aquí vivirá el inventario real. La PC y el Celular leerán y escribirán aquí.
inventario_global = {}

base_datos_mock = {
    "779123455001": {"nombre": "Aceite de Oliva Extra Virgen 1L", "sku": "OLV-29384-MX", "precio": 15.50, "icono": "🍾"},
    "779123455002": {"nombre": "Pasta Integral Penne 500g", "sku": "PST-88210-IT", "precio": 3.25, "icono": "🍝"},
    "779123455003": {"nombre": "Detergente Líquido", "sku": "CLN-00921-ECO", "precio": 12.90, "icono": "🧼"},
    "779123455004": {"nombre": "Cereales de Avena y Miel", "sku": "CRV-77321-US", "precio": 6.75, "icono": "🥣"},
    "779123455005": {"nombre": "Café Molido Tostado Oscuro", "sku": "COF-55219-BR", "precio": 18.20, "icono": "☕"}
}

# ==========================================
# 1. HTML DE LA PC (DASHBOARD PRINCIPAL)
# ==========================================
HTML_PC = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Piolamart - Caja Principal</title>
    <style>
        :root { --bg-color: #f8f9fa; --card-bg: #ffffff; --text-main: #1f2937; --text-muted: #6b7280; --border-color: #e5e7eb; --primary: #2563eb; --danger: #ef4444; --success: #10b981; }
        body { font-family: 'Segoe UI', Tahoma, sans-serif; background-color: var(--bg-color); color: var(--text-main); margin: 0; padding: 20px; }
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
        .header h1 { margin: 0; font-size: 24px; display: flex; align-items: center; gap: 10px; }
        .btn { padding: 10px 15px; border: 1px solid var(--border-color); background: var(--card-bg); border-radius: 8px; cursor: pointer; font-weight: 600; transition: 0.2s; }
        .btn:hover { background: #f3f4f6; }
        .btn-link { background: #8b5cf6; color: white; border: none; }
        .btn-link:hover { background: #7c3aed; }
        .btn-danger { background: var(--danger); color: white; border: none; }
        .main-card { background: var(--card-bg); border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th { text-align: left; padding: 12px; color: var(--text-muted); font-size: 12px; border-bottom: 2px solid var(--border-color); }
        td { padding: 15px 12px; border-bottom: 1px solid var(--border-color); vertical-align: middle; }
        .product-cell { display: flex; align-items: center; gap: 15px; }
        .product-icon { font-size: 24px; background: var(--bg-color); padding: 10px; border-radius: 8px; }
        .summary-card { position: fixed; bottom: 30px; right: 30px; background: var(--card-bg); padding: 20px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.15); width: 250px; border: 2px solid var(--primary); }
        .summary-total { display: flex; justify-content: space-between; align-items: center; font-size: 24px; font-weight: bold; color: var(--text-main); margin-top: 10px;}
        
        /* Modal del QR para vincular celular */
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); align-items: center; justify-content: center; }
        .modal-content { background: white; padding: 30px; border-radius: 16px; text-align: center; }
        .modal-content img { border: 4px solid var(--border-color); border-radius: 12px; margin: 15px 0; }
    </style>
</head>
<body>

    <div class="header">
        <h1>🖥️ Piolamart - Caja Principal</h1>
        <div style="display: flex; gap: 10px;">
            <button class="btn btn-danger" onclick="limpiarServer()">🗑️ Limpiar Caja</button>
            <button class="btn btn-link" onclick="mostrarQR()">📱 Vincular Pistolete (Celular)</button>
        </div>
    </div>

    <div class="main-card">
        <table>
            <thead>
                <tr>
                    <th>Producto & SKU</th>
                    <th>P. Unitario</th>
                    <th>Cantidad</th>
                    <th>Subtotal</th>
                </tr>
            </thead>
            <tbody id="tabla-body">
                <tr><td colspan="4" style="text-align: center; padding: 30px;">Esperando escaneos desde el celular... ⏳</td></tr>
            </tbody>
        </table>
    </div>

    <div class="summary-card">
        <div style="font-size: 12px; font-weight: bold; color: var(--text-muted);">RESUMEN EN VIVO</div>
        <div class="summary-total">
            <span>Total:</span>
            <span id="total-price" style="color: var(--primary);">$0.00</span>
        </div>
    </div>

    <div id="qrModal" class="modal" onclick="this.style.display='none'">
        <div class="modal-content" onclick="event.stopPropagation()">
            <h2>Escanea para usar como Pistolete</h2>
            <p>Abre la cámara de tu celular y escanea este código.</p>
            <img id="qrImage" src="" alt="Código QR de Enlace">
            <br>
            <button class="btn" onclick="document.getElementById('qrModal').style.display='none'">Cerrar</button>
        </div>
    </div>

    <script>
        // Función para mostrar el QR con TU IP FIJA
        function mostrarQR() {
            // AQUÍ ESTÁ LA MAGIA: Forzamos tu IP real para que el QR nunca se equivoque
            let urlActual = 'https://10.10.28.132:5000/pistolete';
            
            document.getElementById('qrImage').src = "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=" + encodeURIComponent(urlActual);
            document.getElementById('qrModal').style.display = 'flex';
        }

        // ==========================================
        // MAGIA DE SINCRONIZACIÓN (POLLING)
        // ==========================================
        function cargarInventario() {
            fetch('/api/inventario')
                .then(res => res.json())
                .then(data => {
                    const tbody = document.getElementById('tabla-body');
                    let totalPrice = 0;
                    
                    if (Object.keys(data).length === 0) {
                        tbody.innerHTML = '<tr><td colspan="4" style="text-align: center; padding: 30px; color: #6b7280;">Esperando escaneos desde el celular... ⏳</td></tr>';
                        document.getElementById('total-price').innerText = '$0.00';
                        return;
                    }

                    tbody.innerHTML = ''; // Limpiamos tabla
                    
                    for (const [codigo, item] of Object.entries(data)) {
                        let subtotal = item.precio * item.cantidad;
                        totalPrice += subtotal;

                        let row = `
                            <tr>
                                <td>
                                    <div class="product-cell">
                                        <div class="product-icon">${item.icono}</div>
                                        <div>
                                            <h4 style="margin:0;">${item.nombre}</h4>
                                            <p style="margin:0; font-size:12px; color:gray;">${item.sku} | Cod: ${codigo}</p>
                                        </div>
                                    </div>
                                </td>
                                <td>$${item.precio.toFixed(2)}</td>
                                <td style="font-weight: bold; font-size: 18px;">${item.cantidad}</td>
                                <td style="font-weight: bold; color: #2563eb;">$${subtotal.toFixed(2)}</td>
                            </tr>
                        `;
                        tbody.innerHTML += row;
                    }
                    document.getElementById('total-price').innerText = `$${totalPrice.toFixed(2)}`;
                });
        }

        function limpiarServer() {
            if(confirm("¿Borrar todo el inventario de la caja?")) {
                fetch('/api/limpiar', {method: 'POST'}).then(() => cargarInventario());
            }
        }

        // Le preguntamos al servidor cada 1.5 segundos si hay algo nuevo
        setInterval(cargarInventario, 1500);
        cargarInventario(); // Carga inicial
    </script>
</body>
</html>
"""

# ==========================================
# 2. HTML DEL CELULAR (EL PISTOLETE)
# ==========================================
# ==========================================
# 2. HTML DEL CELULAR (EL PISTOLETE - BLOQUEA URLs)
# ==========================================
HTML_CELULAR = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Pistolete - Piolamart</title>
    <script src="https://unpkg.com/html5-qrcode"></script>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #111827; color: white; text-align: center; margin: 0; padding: 20px; }
        #reader { width: 100%; max-width: 500px; margin: 0 auto; border-radius: 12px; overflow: hidden; border: 2px solid #374151 !important; background: black; }
        .status-box { margin-top: 20px; padding: 15px; border-radius: 8px; background: #1f2937; border: 2px solid #374151; }
        .success { border-color: #10b981; color: #10b981; }
        .error { border-color: #ef4444; color: #ef4444; }
    </style>
</head>
<body>
    <h2 style="color: #3b82f6; margin-top:0;">📱 Pistolete Conectado</h2>
    <p style="color: gray; font-size: 14px;">Apunta el código de barras. (Los enlaces QR serán ignorados).</p>
    
    <div id="reader"></div>
    
    <div id="status" class="status-box">Listo para escanear...</div>

    <script>
        let ultimoEscaneo = 0;

        function onScanSuccess(decodedText) {
            let ahora = Date.now();
            if (ahora - ultimoEscaneo < 1500) return; // Evita escanear a lo loco
            ultimoEscaneo = ahora;

            let statusBox = document.getElementById('status');

            // --- FILTRO ANTI-URLs ---
            let esEnlace = false;
            try {
                let url = new URL(decodedText);
                esEnlace = (url.protocol === "http:" || url.protocol === "https:");
            } catch (_) {
                esEnlace = false; // Si truena, no es URL válida, es texto normal
            }

            // Si es un enlace, mostramos advertencia y paramos aquí.
            if (esEnlace) {
                statusBox.innerHTML = `🚫 <b>Enlace Ignorado</b><br>Solo se permiten códigos de productos.`;
                statusBox.className = "status-box error";
                
                // Vibración cortita de error (si el cel lo soporta)
                if (navigator.vibrate) navigator.vibrate([50, 50, 50]); 
                return; // Cortamos la función para que no mande nada a la PC
            }

            // Si pasa el filtro, sigue el proceso normal:
            if (navigator.vibrate) navigator.vibrate(200);

            statusBox.innerHTML = `⏳ Enviando: ${decodedText}...`;
            statusBox.className = "status-box";

            // MANDAR AL SERVIDOR (LA PC)
            fetch('/api/escanear', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ codigo: decodedText })
            })
            .then(res => res.json())
            .then(data => {
                statusBox.innerHTML = `✅ ¡Enviado a la PC!<br><b style="font-size:20px;">${data.producto}</b>`;
                statusBox.className = "status-box success";
            })
            .catch(err => {
                statusBox.innerHTML = `❌ Error de conexión`;
                statusBox.className = "status-box error";
            });
        }

        let html5QrcodeScanner = new Html5QrcodeScanner(
            "reader", 
            { fps: 10, qrbox: { width: 250, height: 150 }, videoConstraints: { facingMode: "environment" } }, 
            false
        );
        html5QrcodeScanner.render(onScanSuccess, () => {});
    </script>
</body>
</html>
"""

# ==========================================
# RUTAS DE FLASK (APIs y PÁGINAS)
# ==========================================

# 1. Página de la PC (Dashboard)
@app.route("/")
def index():
    return render_template_string(HTML_PC)

# 2. Página del Celular (Pistolete)
@app.route("/pistolete")
def pistolete():
    return render_template_string(HTML_CELULAR)

# 3. API: La PC pide el inventario
@app.route("/api/inventario", methods=["GET"])
def get_inventario():
    return jsonify(inventario_global)

# 4. API: La PC borra todo
@app.route("/api/limpiar", methods=["POST"])
def limpiar_inventario():
    inventario_global.clear()
    return jsonify({"status": "ok"})

# 5. API: El Celular manda un código escaneado
@app.route("/api/escanear", methods=["POST"])
def recibir_escaneo():
    data = request.json
    codigo = data.get("codigo", "")

    if codigo in inventario_global:
        inventario_global[codigo]["cantidad"] += 1
        nombre_producto = inventario_global[codigo]["nombre"]
    else:
        # Busca en BD simulada o crea genérico
        info = base_datos_mock.get(codigo)
        if not info:
            info = {"nombre": "Producto Genérico", "sku": f"DESC-{codigo[:6]}", "precio": 5.00, "icono": "📦"}
        
        inventario_global[codigo] = {
            "nombre": info["nombre"],
            "sku": info["sku"],
            "precio": info["precio"],
            "icono": info["icono"],
            "cantidad": 1
        }
        nombre_producto = info["nombre"]

    return jsonify({"status": "ok", "producto": nombre_producto})

if __name__ == "__main__":
    # HOST='0.0.0.0' para que se vean en la red, SSL para la cámara del cel.
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context='adhoc')
