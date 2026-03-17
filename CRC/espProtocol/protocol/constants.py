# CRC-16/CCITT-FALSE algorithm parameters
CRCBEGIN = 0xFFFF
POLY = 0x1021

# Protocol frame
START = 0xAA

# Message types
TYPE_CONFIG = 0x01
TYPE_READ   = 0x02
TYPE_WRITE  = 0x03
TYPE_EVENT  = 0x04
TYPE_ERROR  = 0xFF

# Peripherals
PERIPHERAL_GPIO   = 0x01
PERIPHERAL_DAC    = 0x02
PERIPHERAL_MODBUS = 0x03
PERIPHERAL_SYS    = 0xFF

# Response status
STATUS_OK   = 0x00
STATUS_FAIL = 0xFF

# CONFIG byte — encodes GPIO pin configuration in a single byte
# Format: CONFIG_<direction>_<resistor>_<trigger>
#
# Direction:  OUT = output         | IN  = input
# Resistor:   OD  = open-drain     | PP  = push-pull      (output)
#             PU  = pull-up        | PD  = pull-down      (input)
#             NP  = no pull
# Trigger:    HIGH / LOW           (output level)
#             R   = rising edge    | F   = falling edge   (input interrupt)
#             B   = both edges
# Interrupt:  NI  = no interrupt   | WI  = with interrupt (input only)
#
# Reference table:
# Value | Direction | Interrupt | Resistor | Level/Trigger
# 0x01  | OUT       | -         | OD       | HIGH
# 0x02  | OUT       | -         | PP       | HIGH
# 0x03  | OUT       | -         | OD       | LOW
# 0x04  | OUT       | -         | PP       | LOW
# 0x05  | IN        | NI        | PU       | -
# 0x06  | IN        | NI        | PD       | -
# 0x07  | IN        | NI        | NP       | -
# 0x08  | IN        | WI        | PU       | R
# 0x09  | IN        | WI        | PU       | F
# 0x0A  | IN        | WI        | PU       | B
# 0x0B  | IN        | WI        | PD       | R
# 0x0C  | IN        | WI        | PD       | F
# 0x0D  | IN        | WI        | PD       | B
# 0x0E  | IN        | WI        | NP       | R
# 0x0F  | IN        | WI        | NP       | F
# 0x10  | IN        | WI        | NP       | B
CONFIG_OUT_OD_HIGH  = 0x01
CONFIG_OUT_PP_HIGH  = 0x02
CONFIG_OUT_OD_LOW   = 0x03
CONFIG_OUT_PP_LOW   = 0x04
CONFIG_IN_NI_PU     = 0x05
CONFIG_IN_NI_PD     = 0x06
CONFIG_IN_NI_NP     = 0x07
CONFIG_IN_WI_PU_R   = 0x08
CONFIG_IN_WI_PU_F   = 0x09
CONFIG_IN_WI_PU_B   = 0x0A
CONFIG_IN_WI_PD_R   = 0x0B
CONFIG_IN_WI_PD_F   = 0x0C
CONFIG_IN_WI_PD_B   = 0x0D
CONFIG_IN_WI_NP_R   = 0x0E
CONFIG_IN_WI_NP_F   = 0x0F
CONFIG_IN_WI_NP_B   = 0x10