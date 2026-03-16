import protocol
import utils

pacote = protocol.build_packet(protocol.TYPE_WRITE, protocol.PERIPHERAL_GPIO, b'\x0A\x01')

utils.print_packet(pacote)
