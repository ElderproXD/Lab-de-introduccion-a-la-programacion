from flask import Flask, render_template_string, request, jsonify
import sqlite3
import json
import csv
import os

app = Flask(__name__)
app.secret_key = "clave_secreta_2026"

# ==========================================
# MOTOR DE BASES DE DATOS (Persistencia Triple)
# ==========================================
inventario_global = {}

base_datos_mock = {
    "779123455001": {"nombre": "Aceite de Oliva Extra Virgen 1L", "sku": "OLV-29384-MX", "precio": 15.50, "icono": "🍾"},
    "779123455002": {"nombre": "Pasta Integral Penne 500g", "sku": "PST-88210-IT", "precio": 3.25, "icono": "🍝"},
    "779123455003": {"nombre": "Detergente Líquido", "sku": "CLN-00921-ECO", "precio": 12.90, "icono": "🧼"},
    "779123455004": {"nombre": "Cereales de Avena y Miel", "sku": "CRV-77321-US", "precio": 6.75, "icono": "🥣"},
    "779123455005": {"nombre": "Café Molido Tostado Oscuro", "sku": "COF-55219-BR", "precio": 18.20, "icono": "☕"}
}

def init_db():
    conn = sqlite3.connect('piolamart.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS inventario
                 (codigo TEXT PRIMARY KEY, nombre TEXT, sku TEXT, precio REAL, cantidad INTEGER, icono TEXT)''')
    conn.commit()
    conn.close()

def cargar_datos_inicio():
    global inventario_global
    if os.path.exists('inventario.json'):
        with open('inventario.json', 'r', encoding='utf-8') as f:
            try:
                inventario_global = json.load(f)
            except:
                inventario_global = {}

def guardar_en_las_3_bases():
    # 1. JSON
    with open('inventario.json', 'w', encoding='utf-8') as f:
        json.dump(inventario_global, f, ensure_ascii=False, indent=4)
        
    # 2. CSV
    with open('inventario.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Codigo_Barras', 'Nombre', 'SKU', 'Precio', 'Stock', 'Valor_Total'])
        for cod, item in inventario_global.items():
            writer.writerow([cod, item['nombre'], item['sku'], item['precio'], item['cantidad'], item['precio']*item['cantidad']])
            
    # 3. SQLite
    conn = sqlite3.connect('piolamart.db')
    c = conn.cursor()
    c.execute('DELETE FROM inventario')
    for cod, item in inventario_global.items():
        c.execute('INSERT INTO inventario (codigo, nombre, sku, precio, cantidad, icono) VALUES (?,?,?,?,?,?)',
                  (cod, item['nombre'], item['sku'], item['precio'], item['cantidad'], item['icono']))
    conn.commit()
    conn.close()

init_db()
cargar_datos_inicio()

# ==========================================
# 1. HTML DE LA PC (PANEL ADMIN CON AUTO-MODAL Y BORRADO)
# ==========================================
HTML_PC = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Piolamart Pro - DB Admin</title>
    <style>
        body { margin: 0; font-family: 'Segoe UI', Tahoma, sans-serif; background-color: #f1f5f9; color: #334155; display: flex; height: 100vh; }
        .sidebar { width: 260px; background-color: #0f172a; color: white; padding: 20px; display: flex; flex-direction: column; }
        .sidebar h2 { color: #38bdf8; font-size: 22px; margin-top: 0; border-bottom: 1px solid #334155; padding-bottom: 15px; }
        .db-status { background: #1e293b; padding: 15px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #10b981; }
        .db-item { display: flex; justify-content: space-between; font-size: 14px; margin-bottom: 8px; }
        .status-dot { color: #10b981; font-weight: bold; }
        .btn-vincular { background-color: #3b82f6; color: white; border: none; padding: 12px; border-radius: 8px; font-weight: bold; cursor: pointer; width: 100%; margin-top: auto; }
        .btn-danger-main { background-color: #ef4444; color: white; border: none; padding: 12px; border-radius: 8px; font-weight: bold; cursor: pointer; width: 100%; margin-top: 10px; }
        
        .main-content { flex-grow: 1; padding: 30px; overflow-y: auto; }
        .stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 30px; }
        .stat-card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; }
        .stat-card h3 { margin: 0 0 5px 0; color: #64748b; font-size: 12px; text-transform: uppercase; }
        .stat-card p { margin: 0; font-size: 24px; font-weight: bold; }

        .table-container { background: white; border-radius: 10px; border: 1px solid #e2e8f0; overflow: hidden; }
        table { width: 100%; border-collapse: collapse; }
        th { padding: 15px 20px; background-color: #f8fafc; color: #475569; font-size: 13px; text-align: left; border-bottom: 2px solid #e2e8f0; }
        td { padding: 15px 20px; border-bottom: 1px solid #e2e8f0; }
        
        /* Botones de acción en la tabla */
        .acciones-cell { display: flex; gap: 8px; }
        .btn-edit { background: #f1f5f9; border: 1px solid #cbd5e1; padding: 6px 12px; border-radius: 5px; cursor: pointer; font-size: 12px; font-weight: bold; color: #0f172a; }
        .btn-edit:hover { background: #e2e8f0; }
        .btn-delete { background: #fee2e2; border: 1px solid #fca5a5; padding: 6px 12px; border-radius: 5px; cursor: pointer; font-size: 12px; font-weight: bold; color: #dc2626; }
        .btn-delete:hover { background: #fecaca; }

        /* MODALES */
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); align-items: center; justify-content: center; z-index: 1000; }
        .modal-content { background: white; padding: 30px; border-radius: 12px; width: 100%; max-width: 450px; }
        .modal-content h2 { margin-top: 0; color: #0f172a; }
        .form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
        .form-group { margin-bottom: 15px; }
        .form-group.full-width { grid-column: span 2; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: bold; font-size: 13px; color: #475569; }
        .form-group input { width: 100%; padding: 10px; border: 1px solid #cbd5e1; border-radius: 6px; box-sizing: border-box; font-family: inherit; }
        .modal-actions { display: flex; gap: 10px; margin-top: 20px; }
        .btn-save { background: #10b981; color: white; border: none; padding: 12px; flex: 1; border-radius: 6px; font-weight: bold; cursor: pointer; }
        .btn-cancel { background: #94a3b8; color: white; border: none; padding: 12px; flex: 1; border-radius: 6px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>

    <div class="sidebar">
        <h2>📦 Piolamart Pro</h2>
        <div class="db-status">
            <h4>Sincronización Activa</h4>
            <div class="db-item"><span>SQLite (.db)</span> <span class="status-dot">●</span></div>
            <div class="db-item"><span>Excel (.csv)</span> <span class="status-dot">●</span></div>
            <div class="db-item"><span>JSON (.json)</span> <span class="status-dot">●</span></div>
        </div>
        <button class="btn-vincular" onclick="mostrarQR()">📱 Vincular Celular</button>
        <button class="btn-danger-main" onclick="limpiarServer()">⚠️ Vaciar Bases de Datos</button>
    </div>

    <div class="main-content">
        <h1>Gestión de Inventario en Tiempo Real</h1>
        <div class="stats-grid">
            <div class="stat-card"><h3>Registros Únicos</h3><p id="total-registros">0</p></div>
            <div class="stat-card"><h3>Stock Total</h3><p id="total-stock">0</p></div>
            <div class="stat-card"><h3>Valor de Inventario</h3><p id="total-valor" style="color: #10b981;">$0.00</p></div>
        </div>

        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>Cód. Barras</th>
                        <th>Producto</th>
                        <th>SKU</th>
                        <th>Precio</th>
                        <th>Stock</th>
                        <th>Subtotal</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody id="tabla-body"></tbody>
            </table>
        </div>
    </div>

    <div id="editModal" class="modal">
        <div class="modal-content">
            <h2>✏️ Modificar Parámetros</h2>
            <input type="hidden" id="edit-old-codigo">
            
            <div class="form-grid">
                <div class="form-group full-width">
                    <label>Código de Barras (Modificable)</label>
                    <input type="text" id="edit-codigo" style="font-family: monospace; font-weight: bold; color: #0284c7; background: #f0f9ff;">
                </div>
                
                <div class="form-group full-width">
                    <label>Nombre del Producto</label>
                    <input type="text" id="edit-nombre">
                </div>

                <div class="form-group full-width">
                    <label>SKU (Personalizado)</label>
                    <input type="text" id="edit-sku">
                </div>

                <div class="form-group">
                    <label>Precio Unitario ($)</label>
                    <input type="number" step="0.01" id="edit-precio">
                </div>
                
                <div class="form-group">
                    <label>Unidades (Stock)</label>
                    <input type="number" id="edit-cantidad">
                </div>
            </div>

            <div class="modal-actions">
                <button class="btn-save" onclick="guardarEdicion()">Guardar Cambios</button>
                <button class="btn-cancel" onclick="cerrarModal('editModal')">Cancelar</button>
            </div>
        </div>
    </div>

    <div id="qrModal" class="modal">
        <div class="modal-content" style="text-align: center;">
            <h2>📱 Enlace de Pistolete</h2>
            <img id="qrImage" src="" style="width: 200px; margin: 20px 0;">
            <button class="btn-cancel" style="width: 100%;" onclick="cerrarModal('qrModal')">Cerrar</button>
        </div>
    </div>

    <script>
        let inventarioAnterior = null; // Memoria para detectar productos nuevos

        function mostrarQR() {
            let urlActual = 'https://10.10.28.132:5000/pistolete';
            document.getElementById('qrImage').src = "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=" + encodeURIComponent(urlActual);
            document.getElementById('editModal').style.display = 'none';
            document.getElementById('qrModal').style.display = 'flex';
        }

        function abrirEditor(codigo, nombre, sku, precio, cantidad) {
            document.getElementById('edit-old-codigo').value = codigo;
            document.getElementById('edit-codigo').value = codigo;
            document.getElementById('edit-nombre').value = nombre;
            document.getElementById('edit-sku').value = sku;
            document.getElementById('edit-precio').value = precio;
            document.getElementById('edit-cantidad').value = cantidad;
            document.getElementById('editModal').style.display = 'flex';
        }

        function cerrarModal(id) { document.getElementById(id).style.display = 'none'; }

        function guardarEdicion() {
            const data = {
                old_codigo: document.getElementById('edit-old-codigo').value,
                new_codigo: document.getElementById('edit-codigo').value,
                nombre: document.getElementById('edit-nombre').value,
                sku: document.getElementById('edit-sku').value,
                precio: parseFloat(document.getElementById('edit-precio').value),
                cantidad: parseInt(document.getElementById('edit-cantidad').value)
            };

            fetch('/api/editar', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            }).then(() => {
                cerrarModal('editModal');
                cargarInventario();
            });
        }

        function eliminarProducto(codigo) {
            if(confirm("🗑️ ¿Eliminar permanentemente este producto de las bases de datos?")) {
                fetch('/api/eliminar', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ codigo: codigo })
                }).then(() => cargarInventario());
            }
        }

        function cargarInventario() {
            fetch('/api/inventario')
                .then(res => res.json())
                .then(data => {
                    // --- LÓGICA DE AUTO-APERTURA PARA PRODUCTOS NUEVOS ---
                    if (inventarioAnterior !== null && document.getElementById('editModal').style.display !== 'flex') {
                        let llavesNuevas = Object.keys(data);
                        let llavesViejas = Object.keys(inventarioAnterior);
                        
                        // Buscamos si hay un código que no estaba en el ciclo anterior
                        let agregados = llavesNuevas.filter(k => !llavesViejas.includes(k));
                        
                        if (agregados.length > 0) {
                            let codigoNuevo = agregados[agregados.length - 1];
                            let item = data[codigoNuevo];
                            
                            // Si es un producto que no estaba en la base de datos simulada
                            if (item.nombre.includes("Genérico")) {
                                abrirEditor(codigoNuevo, "", item.sku, 0, item.cantidad);
                            }
                        }
                    }
                    inventarioAnterior = data; // Guardamos foto actual para comparar luego

                    // --- RENDERIZAR LA TABLA ---
                    const tbody = document.getElementById('tabla-body');
                    let totalR = 0, totalS = 0, valorV = 0;
                    tbody.innerHTML = '';
                    
                    if (Object.keys(data).length === 0) {
                        tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; padding: 40px; color: #94a3b8;">La base de datos está vacía. Escanea un producto con el celular.</td></tr>';
                    } else {
                        for (const [cod, item] of Object.entries(data)) {
                            let sub = item.precio * item.cantidad;
                            totalR++; totalS += item.cantidad; valorV += sub;

                            tbody.innerHTML += `
                                <tr>
                                    <td><span style="background:#e0f2fe; color:#0284c7; padding:4px 8px; border-radius:4px; font-family:monospace;">${cod}</span></td>
                                    <td>${item.icono} <b>${item.nombre}</b></td>
                                    <td style="color:#64748b; font-size:13px;">${item.sku}</td>
                                    <td>$${item.precio.toFixed(2)}</td>
                                    <td><b>${item.cantidad}</b></td>
                                    <td><b style="color:#0f172a;">$${sub.toFixed(2)}</b></td>
                                    <td>
                                        <div class="acciones-cell">
                                            <button class="btn-edit" onclick="abrirEditor('${cod}', '${item.nombre}', '${item.sku}', ${item.precio}, ${item.cantidad})">✏️</button>
                                            <button class="btn-delete" onclick="eliminarProducto('${cod}')">🗑️</button>
                                        </div>
                                    </td>
                                </tr>`;
                        }
                    }
                    
                    document.getElementById('total-registros').innerText = totalR;
                    document.getElementById('total-stock').innerText = totalS;
                    document.getElementById('total-valor').innerText = `$${valorV.toFixed(2)}`;
                });
        }

        function limpiarServer() {
            if(confirm("⚠️ ¿Seguro que quieres borrar TODA la información de las bases de datos?")) {
                fetch('/api/limpiar', {method: 'POST'}).then(() => {
                    inventarioAnterior = {}; // Reseteamos la memoria local también
                    cargarInventario();
                });
            }
        }

        setInterval(cargarInventario, 1500);
        cargarInventario();
    </script>
</body>
</html>
"""

# ==========================================
# 2. HTML DEL CELULAR (PISTOLETE)
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
        body { font-family: sans-serif; background: #0f172a; color: white; text-align: center; margin: 0; padding: 20px; }
        #reader { width: 100%; border-radius: 12px; overflow: hidden; border: 2px solid #334155 !important; background: black; }
        .status { margin-top: 20px; padding: 15px; border-radius: 8px; background: #1e293b; border: 2px solid #334155; }
    </style>
</head>
<body>
    <h2 style="color: #38bdf8;">📱 Pistolete DB</h2>
    <div id="reader"></div>
    <div id="status" class="status">Listo para escanear...</div>

    <script>
        let ultimo = 0;
        function onScanSuccess(text) {
            if (Date.now() - ultimo < 1500) return;
            ultimo = Date.now();
            
            try { new URL(text); return; } catch(_) {}

            if (navigator.vibrate) navigator.vibrate(200);
            document.getElementById('status').innerText = "Guardando en DB...";

            fetch('/api/escanear', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ codigo: text })
            }).then(res => res.json()).then(data => {
                document.getElementById('status').innerHTML = "✅ Guardado: <br>" + data.producto;
            });
        }
        let scanner = new Html5QrcodeScanner("reader", { fps: 10, qrbox: 250 }, false);
        scanner.render(onScanSuccess, () => {});
    </script>
</body>
</html>
"""

# ==========================================
# RUTAS DE FLASK (CRUD COMPLETO)
# ==========================================

@app.route("/")
def index():
    return render_template_string(HTML_PC)

@app.route("/pistolete")
def pistolete():
    return render_template_string(HTML_CELULAR)

@app.route("/api/inventario")
def get_inv():
    return jsonify(inventario_global)

@app.route("/api/limpiar", methods=["POST"])
def limpiar():
    inventario_global.clear()
    guardar_en_las_3_bases()
    return jsonify({"status": "ok"})

@app.route("/api/eliminar", methods=["POST"])
def eliminar_producto():
    data = request.json
    codigo = data.get("codigo")
    if codigo in inventario_global:
        del inventario_global[codigo]
        guardar_en_las_3_bases() # Borramos de SQLite, JSON y CSV
    return jsonify({"status": "ok"})

@app.route("/api/escanear", methods=["POST"])
def escanear():
    data = request.json
    cod = data.get("codigo", "")
    if cod in inventario_global:
        inventario_global[cod]["cantidad"] += 1
    else:
        info = base_datos_mock.get(cod, {"nombre": "Genérico (Editar)", "sku": f"DESC-{cod[:6]}", "precio": 0.0, "icono": "📦"})
        inventario_global[cod] = {**info, "cantidad": 1}
    guardar_en_las_3_bases()
    return jsonify({"status": "ok", "producto": inventario_global[cod]["nombre"]})

@app.route("/api/editar", methods=["POST"])
def editar_producto():
    data = request.json
    old_cod = data.get("old_codigo")
    new_cod = data.get("new_codigo")
    
    if old_cod in inventario_global:
        item = inventario_global.pop(old_cod) 
        
        # Validamos que no llegue un nombre vacío
        nombre = data.get("nombre").strip()
        item["nombre"] = nombre if nombre else "Producto sin nombre"
        
        item["sku"] = data.get("sku")
        item["precio"] = float(data.get("precio"))
        item["cantidad"] = int(data.get("cantidad"))
        
        inventario_global[new_cod] = item
        guardar_en_las_3_bases() 
        return jsonify({"status": "ok"})
        
    return jsonify({"status": "error"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context='adhoc')
