#!/usr/bin/env python3
import serial
import time
from serial.tools import list_ports


def find_arduino():
    """Busca automáticamente el puerto del Arduino"""
    ports = list_ports.comports()
    for port in ports:
        if 'Arduino' in port.description or 'USB' in port.description:
            return port.device
    return None


def main():
    port = find_arduino() or '/dev/ttyUSB0'
    baudrate = 9600

    print(f"Conectando a {port}...")

    try:
        ser = serial.Serial(port, baudrate, timeout=0.1)
        time.sleep(2)  # Tiempo de inicialización

        print("Monitor RFID activo. Presiona Ctrl+C para salir")

        while True:
            try:
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8').strip()
                    if line:  # Solo procesar líneas no vacías
                        print("Datos:", line)

                        # Detección de UID (adaptar a tu formato)
                        if "UID:" in line:
                            uid = line.split("UID:")[1].strip()
                            print(f"¡Tarjeta detectada! UID: {uid}")

            except UnicodeDecodeError:
                continue  # Ignorar errores de decodificación

            time.sleep(0.01)  # Pequeña pausa

    except KeyboardInterrupt:
        print("\nPrograma terminado")
    except Exception as e:
        print(f"Error crítico: {e}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Puerto serial cerrado")


if __name__ == "__main__":
    main()
