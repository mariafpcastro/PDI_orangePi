"""
espCRCtry.py

CLI para enviar comandos ao ESP32 via serial e monitorar
continuamente todos os frames recebidos em uma thread separada.
"""

import time
import threading
import serial
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import QAT as ep


# --- Leitura contínua em thread separada ---

def reader_thread(ser: serial.Serial, stop_event: threading.Event) -> None:
    """
    Fica em loop lendo e imprimindo tudo que a ESP32 enviar.
    Roda como daemon — encerra junto com o processo principal.

    Args:
        ser        : porta serial aberta.
        stop_event : sinaliza quando a thread deve encerrar.
    """
    while not stop_event.is_set():
        try:
            raw = ep.read_frame(ser)
        except Exception as e:
            print(f"\n[reader] Erro na leitura: {e}")
            continue

        if raw is None:
            # timeout normal, volta ao início do loop
            continue

        print()  # linha em branco para separar do prompt do usuário

        if not ep.check_packet(raw):
            print("[reader] CRC inválido — frame corrompido.")
            continue

        frame = ep.parse_packet(raw)
        ep.print_frame(frame)

        # Interpreta leitura GPIO se aplicável
        if (frame.get("peripheral") == ep.PERIPHERAL_GPIO
                and frame.get("size", 0) >= 2):
            ep.gpio_read(frame.get("type"), frame["payload"])


# --- Helpers de input do usuário ---

def select_type() -> int:
    options = {
        1: ep.TYPE_CONFIG,
        2: ep.TYPE_READ,
        3: ep.TYPE_WRITE,
        4: ep.TYPE_EVENT,
    }
    print("\nTipo de mensagem:")
    print("  1. Config   2. Read   3. Write   4. Event")
    while True:
        choice = int(input("Selecione: "))
        if choice in options:
            return options[choice]
        print("Valor inválido, tente novamente.")


def select_peripheral() -> int:
    options = {
        1: ep.PERIPHERAL_GPIO,
        2: ep.PERIPHERAL_DAC,
        3: ep.PERIPHERAL_MODBUS,
        4: ep.PERIPHERAL_SYS,
    }
    print("\nPeriferico:")
    print("  1. GPIO   2. DAC   3. Modbus   4. System/Global")
    while True:
        choice = int(input("Selecione: "))
        if choice in options:
            return options[choice]
        print("Valor inválido, tente novamente.")


def select_gpio_config() -> int:
    print("\nDireção:")
    print("  1. Output   2. Input")
    direction = int(input("Selecione: "))

    if direction == 1:
        print("\nResistor:")
        print("  1. Open-drain   2. Push-pull")
        resistor = int(input("Selecione: "))
        print("\nNível:")
        print("  1. High   2. Low")
        level = int(input("Selecione: "))
        table = {
            (1, 1): ep.CONFIG_OUT_OD_HIGH,
            (2, 1): ep.CONFIG_OUT_PP_HIGH,
            (1, 2): ep.CONFIG_OUT_OD_LOW,
            (2, 2): ep.CONFIG_OUT_PP_LOW,
        }
        return table[(resistor, level)]

    else:
        print("\nInterrupção:")
        print("  1. Sem interrupção   2. Com interrupção")
        interrupt = int(input("Selecione: "))
        print("\nResistor:")
        print("  1. Pull-up   2. Pull-down   3. Sem pull")
        resistor = int(input("Selecione: "))

        if interrupt == 1:
            return {1: ep.CONFIG_IN_NI_PU,
                    2: ep.CONFIG_IN_NI_PD,
                    3: ep.CONFIG_IN_NI_NP}[resistor]

        print("\nTrigger:")
        print("  1. Rising   2. Falling   3. Both")
        trigger = int(input("Selecione: "))
        table = {
            (1, 1): ep.CONFIG_IN_WI_PU_R, (1, 2): ep.CONFIG_IN_WI_PU_F,
            (1, 3): ep.CONFIG_IN_WI_PU_B, (2, 1): ep.CONFIG_IN_WI_PD_R,
            (2, 2): ep.CONFIG_IN_WI_PD_F, (2, 3): ep.CONFIG_IN_WI_PD_B,
            (3, 1): ep.CONFIG_IN_WI_NP_R, (3, 2): ep.CONFIG_IN_WI_NP_F,
            (3, 3): ep.CONFIG_IN_WI_NP_B,
        }
        return table[(resistor, trigger)]


def build_payload(per_msg: int, type_msg: int) -> bytes:
    if per_msg == ep.PERIPHERAL_GPIO and type_msg == ep.TYPE_CONFIG:
        pin    = int(input("Número do pino: "))
        config = select_gpio_config()
        return ep.gpio_config_write_payload(pin, config)

    elif per_msg == ep.PERIPHERAL_GPIO and type_msg == ep.TYPE_WRITE:
        pin   = int(input("Número do pino: "))
        level = int(input("Nível (0 = OFF, 1 = ON): "))
        return bytes([pin, level])

    else:
        size = int(input("Tamanho do payload: "))
        return bytes(int(input(f"Byte {i + 1}: ")) for i in range(size))


# --- Main ---

def main():
    ser = serial.Serial("/dev/ttyUSB0", 1_000_000, timeout=1)
    time.sleep(1)

    # Inicia a thread de leitura contínua
    stop_event = threading.Event()
    t = threading.Thread(target=reader_thread, args=(ser, stop_event), daemon=True)
    t.start()
    print("Monitor iniciado. Digite 'q' para sair.\n")

    # Loop de envio de comandos
    while True:
        try:
            cmd = input("\nEnviar novo pacote? [Enter = sim / q = sair]: ").strip().lower()
        except EOFError:
            break

        if cmd == "q":
            break

        try:
            type_msg = select_type()
            per_msg  = select_peripheral()
            payload  = build_payload(per_msg, type_msg)

            packet = ep.build_packet(type_msg, per_msg, payload)
            ep.print_packet(packet)
            ser.write(packet)

        except (ValueError, KeyError) as e:
            print(f"Entrada inválida: {e}. Tente novamente.")

    # Encerra a thread de leitura
    print("\nEncerrando monitor...")
    stop_event.set()
    t.join(timeout=2)
    ser.close()


if __name__ == "__main__":
    main()
'''



"""
espCRCtry.py

CLI para enviar comandos ao ESP32 via serial e monitorar
continuamente todos os frames recebidos em uma thread separada.
"""

import time
import threading
import serial
import sys
import os

#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import QAT as ep

# Lock global para serializar escrita no terminal
_print_lock = threading.Lock()

# Guarda o prompt que está aguardando input no momento (pode ser "")
_current_prompt = ""


def _safe_print(*args, **kwargs) -> None:
    """
    Imprime algo no terminal sem embaralhar o prompt do usuário:
      1. Apaga a linha atual (onde o prompt está piscando).
      2. Imprime o conteúdo desejado.
      3. Reimprime o prompt na última linha, sem \n, para o cursor
         voltar exatamente onde estava.
    """
    with _print_lock:
        # \r volta ao início da linha; espaços apagam o texto anterior
        sys.stdout.write(f"\r{' ' * (len(_current_prompt) + 2)}\r")
        print(*args, **kwargs)
        if _current_prompt:
            sys.stdout.write(_current_prompt)
            sys.stdout.flush()


# --- Leitura contínua em thread separada ---

def reader_thread(ser: serial.Serial, stop_event: threading.Event) -> None:
    """
    Fica em loop lendo e imprimindo tudo que a ESP32 enviar.
    Roda como daemon — encerra junto com o processo principal.

    Args:
        ser        : porta serial aberta.
        stop_event : sinaliza quando a thread deve encerrar.
    """
    while not stop_event.is_set():
        try:
            raw = ep.read_frame(ser)
        except Exception as e:
            _safe_print(f"[reader] Erro na leitura: {e}")
            continue

        if raw is None:
            # timeout normal, volta ao início do loop
            continue

        if not ep.check_packet(raw):
            _safe_print("[reader] CRC inválido — frame corrompido.")
            continue

        frame = ep.parse_packet(raw)

        # Captura o texto de print_frame / gpio_read como string
        # para imprimir tudo de uma vez (evita intercalação parcial)
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            ep.print_frame(frame)
            if (frame.get("peripheral") == ep.PERIPHERAL_GPIO
                    and frame.get("size", 0) >= 2):
                ep.gpio_read(frame.get("type"), frame["payload"])

        _safe_print(buf.getvalue(), end="")


# --- Helpers de input do usuário ---

def select_type() -> int:
    options = {
        1: ep.TYPE_CONFIG,
        2: ep.TYPE_READ,
        3: ep.TYPE_WRITE,
        4: ep.TYPE_EVENT,
    }
    print("\nTipo de mensagem:")
    print("  1. Config   2. Read   3. Write   4. Event")
    while True:
        choice = int(input("Selecione: "))
        if choice in options:
            return options[choice]
        print("Valor inválido, tente novamente.")


def select_peripheral() -> int:
    options = {
        1: ep.PERIPHERAL_GPIO,
        2: ep.PERIPHERAL_DAC,
        3: ep.PERIPHERAL_MODBUS,
        4: ep.PERIPHERAL_SYS,
    }
    print("\nPeriferico:")
    print("  1. GPIO   2. DAC   3. Modbus   4. System/Global")
    while True:
        choice = int(input("Selecione: "))
        if choice in options:
            return options[choice]
        print("Valor inválido, tente novamente.")


def select_gpio_config() -> int:
    print("\nDireção:")
    print("  1. Output   2. Input")
    direction = int(input("Selecione: "))

    if direction == 1:
        print("\nResistor:")
        print("  1. Open-drain   2. Push-pull")
        resistor = int(input("Selecione: "))
        print("\nNível:")
        print("  1. High   2. Low")
        level = int(input("Selecione: "))
        table = {
            (1, 1): ep.CONFIG_OUT_OD_HIGH,
            (2, 1): ep.CONFIG_OUT_PP_HIGH,
            (1, 2): ep.CONFIG_OUT_OD_LOW,
            (2, 2): ep.CONFIG_OUT_PP_LOW,
        }
        return table[(resistor, level)]

    else:
        print("\nInterrupção:")
        print("  1. Sem interrupção   2. Com interrupção")
        interrupt = int(input("Selecione: "))
        print("\nResistor:")
        print("  1. Pull-up   2. Pull-down   3. Sem pull")
        resistor = int(input("Selecione: "))

        if interrupt == 1:
            return {1: ep.CONFIG_IN_NI_PU,
                    2: ep.CONFIG_IN_NI_PD,
                    3: ep.CONFIG_IN_NI_NP}[resistor]

        print("\nTrigger:")
        print("  1. Rising   2. Falling   3. Both")
        trigger = int(input("Selecione: "))
        table = {
            (1, 1): ep.CONFIG_IN_WI_PU_R, (1, 2): ep.CONFIG_IN_WI_PU_F,
            (1, 3): ep.CONFIG_IN_WI_PU_B, (2, 1): ep.CONFIG_IN_WI_PD_R,
            (2, 2): ep.CONFIG_IN_WI_PD_F, (2, 3): ep.CONFIG_IN_WI_PD_B,
            (3, 1): ep.CONFIG_IN_WI_NP_R, (3, 2): ep.CONFIG_IN_WI_NP_F,
            (3, 3): ep.CONFIG_IN_WI_NP_B,
        }
        return table[(resistor, trigger)]


def build_payload(per_msg: int, type_msg: int) -> bytes:
    if per_msg == ep.PERIPHERAL_GPIO and type_msg == ep.TYPE_CONFIG:
        pin    = int(input("Número do pino: "))
        config = select_gpio_config()
        return ep.gpio_config_write_payload(pin, config)

    elif per_msg == ep.PERIPHERAL_GPIO and type_msg == ep.TYPE_WRITE:
        pin   = int(input("Número do pino: "))
        level = int(input("Nível (0 = OFF, 1 = ON): "))
        return bytes([pin, level])

    else:
        size = int(input("Tamanho do payload: "))
        return bytes(int(input(f"Byte {i + 1}: ")) for i in range(size))


# --- Main ---

def main():
    ser = serial.Serial("/dev/ttyUSB0", 1_000_000, timeout=1)
    time.sleep(1)

    # Inicia a thread de leitura contínua
    stop_event = threading.Event()
    t = threading.Thread(target=reader_thread, args=(ser, stop_event), daemon=True)
    t.start()
    print("Monitor iniciado. Digite 'q' para sair.\n")

    # Loop de envio de comandos
    while True:
        try:
            PROMPT = "\nEnviar novo pacote? [Enter = sim / q = sair]: "
            global _current_prompt
            with _print_lock:
                _current_prompt = PROMPT.lstrip("\n")
                sys.stdout.write(PROMPT)
                sys.stdout.flush()
            cmd = sys.stdin.readline().strip().lower()
            with _print_lock:
                _current_prompt = ""
        except EOFError:
            break

        if cmd == "q":
            break

        try:
            type_msg = select_type()
            per_msg  = select_peripheral()
            payload  = build_payload(per_msg, type_msg)

            packet = ep.build_packet(type_msg, per_msg, payload)
            ep.print_packet(packet)
            ser.write(packet)

        except (ValueError, KeyError) as e:
            print(f"Entrada inválida: {e}. Tente novamente.")

    # Encerra a thread de leitura
    print("\nEncerrando monitor...")
    stop_event.set()
    t.join(timeout=2)
    ser.close()


if __name__ == "__main__":
    main()
    '''