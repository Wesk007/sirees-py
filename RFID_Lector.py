#!/usr/bin/env python3
import serial
import time
import requests
import webbrowser
import urllib.parse

# 🌐 URL de tu API (modifica con la IP y ruta correcta)
apiurl = "https://eamisdev.com/api/registro.php"
# 🌐 URL de tu viewer en PHP
viewer_url = "https://eamisdev.com/Proyectos/sirees/view.php"

# 🔍 Detectar automáticamente el puerto del Arduino
def find_arduino():
    from serial.tools import list_ports
    ports = list_ports.comports()
    for port in ports:
        if 'Arduino' in port.description or 'USB' in port.description:
            return port.device
    return None

# 🌐 Enviar UID a la API, esperar JSON y abrir viewer
def enviar_a_api(uid):
    try:
        payload = {"uid": uid}
        r = requests.post(apiurl, json=payload, timeout=5)
        if not r.ok:
            print(f"[✖] Error {r.status_code}: {r.text}")
            return

        # Intentar parsear JSON
        try:
            data = r.json()
            print(f"[→] UID {uid} enviado con éxito. Respuesta JSON:", data)
            status = data.get('status', '')
        except ValueError:
            print("[✖] Error: la respuesta no es un JSON válido.")
            status = ''

        # Construir URL con query params correctamente escapados
        params = {'uid': uid, 'status': status}
        url = f"{viewer_url}?{urllib.parse.urlencode(params)}"
        print(f"[→] Abriendo vista en: {url}")
        webbrowser.open(url)

    except Exception as e:
        print(f"[✖] Excepción al enviar: {e}")

def main():
    #port = find_arduino() or '/dev/ttyUSB0'
    port = '/tmp/ttyV0'  # Cambia esto al puerto correcto si es necesario
    baudrate = 9600
    print(f"Conectando a {port} a {baudrate} baudios...")
    try:
        ser = serial.Serial(port, baudrate, timeout=0.1)
        time.sleep(2)
        print("Esperando tarjetas RFID... (Ctrl+C para salir)")
        while True:
            if ser.in_waiting:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line.startswith("UID:"):
                    uid = line.split("UID:")[1].strip()
                    print(f"Tarjeta detectada: {uid}")
                    enviar_a_api(uid)
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\nSalida por usuario.")
    except Exception as e:
        print(f"[ERROR crítico] {e}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Puerto serial cerrado.")

if __name__ == "__main__":
    main()