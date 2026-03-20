"""
espCRCtry.py

Command-line interface for sending protocol commands to an ESP32 over serial
and receiving / validating the response frame.
"""

import time
import serial
import sys
import os

# add the parent directory to the path so espProtocol can be found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import QAT as ep



# --- User input helpers ---

def select_type() -> int:
    """
    Prompt the user to select a message type.

    Returns:
        int: Selected message type constant (e.g. ep.TYPE_WRITE).
    """
    options = {
        1: ep.TYPE_CONFIG,
        2: ep.TYPE_READ,
        3: ep.TYPE_WRITE,
        4: ep.TYPE_EVENT,
    }
    print("\nMessage type:")
    print("  1. Config   2. Read   3. Write   4. Event")
    while True:
        choice = int(input("Select: "))
        if choice in options:
            return options[choice]
        print("Invalid value, please try again.")


def select_peripheral() -> int:
    """
    Prompt the user to select a target peripheral.

    Returns:
        int: Selected peripheral constant (e.g. ep.PERIPHERAL_GPIO).
    """
    options = {
        1: ep.PERIPHERAL_GPIO,
        2: ep.PERIPHERAL_DAC,
        3: ep.PERIPHERAL_MODBUS,
        4: ep.PERIPHERAL_SYS,
    }
    print("\nPeripheral:")
    print("  1. GPIO   2. DAC   3. Modbus   4. System/Global")
    while True:
        choice = int(input("Select: "))
        if choice in options:
            return options[choice]
        print("Invalid value, please try again.")


def select_gpio_config() -> int:
    """
    Prompt the user to select a GPIO configuration byte
    using the CONFIG_* constants from constants.py.

    Returns:
        int: Selected CONFIG_* constant.
    """
    print("\nDirection:")
    print("  1. Output   2. Input")
    direction = int(input("Select: "))

    if direction == 1:
        print("\nResistor:")
        print("  1. Open-drain   2. Push-pull")
        resistor = int(input("Select: "))
        print("\nLevel:")
        print("  1. High   2. Low")
        level = int(input("Select: "))
        table = {
            (1, 1): ep.CONFIG_OUT_OD_HIGH,
            (2, 1): ep.CONFIG_OUT_PP_HIGH,
            (1, 2): ep.CONFIG_OUT_OD_LOW,
            (2, 2): ep.CONFIG_OUT_PP_LOW,
        }
        return table[(resistor, level)]

    else:
        print("\nInterrupt:")
        print("  1. No interrupt   2. With interrupt")
        interrupt = int(input("Select: "))
        print("\nResistor:")
        print("  1. Pull-up   2. Pull-down   3. No-pull")
        resistor = int(input("Select: "))

        if interrupt == 1:
            table = {
                1: ep.CONFIG_IN_NI_PU,
                2: ep.CONFIG_IN_NI_PD,
                3: ep.CONFIG_IN_NI_NP,
            }
            return table[resistor]

        else:
            print("\nTrigger:")
            print("  1. Rising   2. Falling   3. Both")
            trigger = int(input("Select: "))
            table = {
                (1, 1): ep.CONFIG_IN_WI_PU_R,
                (1, 2): ep.CONFIG_IN_WI_PU_F,
                (1, 3): ep.CONFIG_IN_WI_PU_B,
                (2, 1): ep.CONFIG_IN_WI_PD_R,
                (2, 2): ep.CONFIG_IN_WI_PD_F,
                (2, 3): ep.CONFIG_IN_WI_PD_B,
                (3, 1): ep.CONFIG_IN_WI_NP_R,
                (3, 2): ep.CONFIG_IN_WI_NP_F,
                (3, 3): ep.CONFIG_IN_WI_NP_B,
            }
            return table[(resistor, trigger)]


def build_payload(per_msg: int, type_msg: int) -> bytes:
    """
    Build the payload bytes based on the selected peripheral and message type.

    Args:
        per_msg  (int): Selected peripheral constant.
        type_msg (int): Selected message type constant.

    Returns:
        bytes: Payload ready to pass to build_packet().
    """
    if per_msg == ep.PERIPHERAL_GPIO and type_msg == ep.TYPE_CONFIG:
        pin = int(input("Pin number: "))
        config = select_gpio_config()
        return ep.gpio_config_write_payload(pin, config)

    elif per_msg == ep.PERIPHERAL_GPIO and type_msg == ep.TYPE_WRITE:
        pin   = int(input("Pin number: "))
        level = int(input("Level (0 = OFF, 1 = ON): "))
        
        return bytes([pin, level])

    else:
        size = int(input("Payload size: "))
        return bytes(int(input(f"Byte {i + 1}: ")) for i in range(size))


# --- Main ---

def main():
    ser = serial.Serial("/dev/ttyUSB0", 1_000_000, timeout=1)
    time.sleep(1)

    type_msg = select_type()
    per_msg  = select_peripheral()
    payload  = build_payload(per_msg, type_msg)

    # Build and send packet
    packet = ep.build_packet(type_msg, per_msg, payload)
    ep.print_packet(packet)
    ser.write(packet)

    # Receive and validate response
    print("\nWaiting for ESP32 response...")
    raw = ep.read_frame(ser)

    if raw is None:
        print("Timeout — no response received.")
    elif not ep.check_packet(raw):
        print("CRC error — corrupted frame.")
    else:
        frame = ep.parse_packet(raw)
        ep.print_frame(frame)

        # Interpret GPIO response
        if per_msg == ep.PERIPHERAL_GPIO and frame["size"] >= 2:
            ep.gpio_read(type_msg, frame["payload"])


if __name__ == "__main__":
    main()