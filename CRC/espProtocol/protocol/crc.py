from . import constants
from . import packet

"""
crc.py

Implementation of the CRC-16/CCITT-FALSE checksum algorithm.

Algorithm parameters:
- Polynomial: 0x1021
- Initial value(init): 0xFFFF
- RefIn: False
- RefOut: False
- Final XOR value: 0x0000

The CRC is computed over all bytes in the provided data sequence.
This implementation is commonly used in communication protocols
based on the CCITT standard.
"""


def crc_calc(data):
	#Docstrings
	"""
	Computes the CRC-16 using the CRC-16/CCITT-FALSE standard.

	Args:
		data (list[int] | bytes): Data used to compute the CRC.
	
	Returns
		int: The computed CRC-16 value (16 bits).
	"""

	crc = constants.CRCBEGIN
	poly = constants.POLY

	for byte in data:
		crc ^= (byte << 8)

		for i in range(8):
			if crc & 0x8000:
				crc = (crc << 1) ^ poly

			else:
				crc <<= 1
			crc &= 0xFFFF

	return crc

	def crc_to_bytes():
		return 0
