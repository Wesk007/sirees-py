#!/usr/bin/env python3
import serial
import time
import webbrowser

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

def enviar_a_api(uid):
    # Construir URL del viewer con el UID
    url = f"{viewer_url}?uid={uid}"
    print(f"[→] Abriendo vista en: {url}")
    webbrowser.open(url)

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
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                print(f"[DEBUG] Recibido: {repr(line)}")
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