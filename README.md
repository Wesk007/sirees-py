## Instrucciones para ejecutar el proyecto

### 1. Activar el entorno virtual (venv)

```bash
source venv/bin/activate
```

### 2. Iniciar el servidor Flask (API)

```bash
python Python_API.py
```

### 3. Simular un puerto serial con `socat`

```bash
socat -d -d PTY,link=/tmp/ttyV0 PTY,link=/tmp/ttyV1
```

> `/tmp/ttyV0` será usado por el script Python para leer datos como si fuera un lector RFID real.

### 4. Enviar datos de prueba (imitando un escaneo de tarjeta RFID)

```bash
echo "123" > /tmp/ttyV1
```

> Asegúrate de que tu script esté leyendo desde `/tmp/ttyV0`.