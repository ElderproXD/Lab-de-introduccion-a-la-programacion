# 🏙️ Loquendo City - Aplicación Web con Flask

## 📌 Introducción
Este proyecto consiste en el desarrollo de una aplicación web utilizando Flask, donde se implementa un sistema completo que integra autenticación de usuarios, navegación mediante un dashboard interactivo y un módulo avanzado de escaneo de códigos QR utilizando la cámara del dispositivo.

El sistema no solo cumple funciones básicas, sino que también incorpora medidas de seguridad al manejar enlaces detectados, evitando redirecciones automáticas y mostrando vistas previas controladas.

---

## ⚙️ 1. Configuración Inicial

El sistema comienza importando las librerías necesarias:

    from flask import Flask, render_template_string, request, redirect, url_for, session

Posteriormente se crea la aplicación:

    app = Flask(__name__)

Se define una clave secreta para el manejo de sesiones:

    app.secret_key = "clave_secreta_2026"

Se establecen credenciales básicas para el acceso:

    USUARIO = "admin"
    CONTRASENA = "admin2026"

### 🧠 Explicación
Flask actúa como el motor del servidor. La variable `session` permite guardar información del usuario entre páginas, lo cual es esencial para mantener la sesión iniciada.

---

## 🔐 2. Sistema de Login

El sistema utiliza una ruta principal que maneja métodos GET y POST:

    @app.route("/", methods=["GET", "POST"])

### Funcionamiento:
- El usuario ingresa sus credenciales
- Flask las valida
- Si son correctas, se guarda la sesión
- Si no, se muestra un error


![Entorno virtual activo](/Ejercicio_11/A/inicio.png)

---

## 🏠 3. Dashboard

Una vez autenticado, el usuario accede a un panel principal con diferentes funcionalidades representadas mediante tarjetas.

Estas tarjetas permiten navegar dentro del sistema, destacando el acceso al escáner móvil.


![Entorno virtual activo](/Ejercicio_11/A/tarjetassss.png)

---

## 📱 4. Módulo de Escáner QR

El sistema integra un escáner utilizando JavaScript y la librería html5-qrcode.

### Inicialización:

    let html5QrcodeScanner = new Html5QrcodeScanner("reader", {
        fps: 15,
        qrbox: { width: 280, height: 180 }
    });

### Funcionamiento:
- Activa la cámara trasera
- Detecta códigos QR en tiempo real
- Procesa el contenido escaneado


![Entorno virtual activo](/Ejercicio_11/A/interfazescan.png)


---

## 🔗 5. Validación de Enlaces

El sistema verifica si el contenido escaneado es un enlace válido:

    let url = new URL(decodedText);

Si es un enlace:
- No lo abre automáticamente
- Muestra advertencia de seguridad
- Permite vista previa


![Entorno virtual activo](/Ejercicio_11/A/link.png)

---

## 👁️ 6. Vista Previa Segura

Se utiliza un iframe para mostrar el contenido:

    iframe.src = url;

Esto evita redirecciones peligrosas y mantiene al usuario dentro del sistema.
/Ejercicio_11/A/vitsa.png

---

## 🔢 7. Lectura de Datos Simples

Si el código no es un enlace, simplemente se muestra el contenido escaneado:

📸 Evidencia:
![Entorno virtual activo](/Ejercicio_11/A/escaneobarras.png)

---

## 🌐 8. Rutas del Servidor

Login:

    @app.route("/", methods=["GET", "POST"])

Escáner:

    @app.route("/escaner")

Logout:

    @app.route("/logout")

---

## 🔒 9. Seguridad Implementada

- Uso de sesiones
- Protección de rutas
- Validación de enlaces
- Vista previa controlada

---

## 🚀 10. Ejecución del Sistema

    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context='adhoc')

El uso de HTTPS es necesario para permitir el acceso a la cámara en navegadores modernos.

---

## 🧩 Conclusión

Este proyecto demuestra la integración completa de:
- Backend con Flask
- Frontend con HTML/CSS
- Funcionalidad avanzada con JavaScript

Además, implementa buenas prácticas de seguridad al manejar contenido externo.
