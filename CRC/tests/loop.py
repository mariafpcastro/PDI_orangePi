import serial
import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import QAT as ep

def main():
    ser = serial.Serial("/dev/ttyUSB0", 1_000_000, timeout=0.1)
    time.sleep(1)
    print("Aguardando frames da ESP32... (Ctrl+C para sair)\n")

    count = 0
    try:
        while True:
            raw = ep.read_frame(ser)
            if raw is None:
                continue

            count += 1
            print(f"[{count}] Frame recebido: {raw.hex(' ').upper()}")

            if not ep.check_packet(raw):
                print("     ^ CRC inválido!")
                continue

            frame = ep.parse_packet(raw)
            if frame.get("peripheral") == ep.PERIPHERAL_GPIO and frame.get("size", 0) >= 2:
                ep.gpio_read(frame["type"], frame["payload"])

    except KeyboardInterrupt:
        print(f"\nEncerrado. Total de frames recebidos: {count}")
        ser.close()

if __name__ == "__main__":
    main()