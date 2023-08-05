import math

class Colour:
	def __init__(self, red=0, green=0, blue=0):
		if type(red) == str:
			self.hex = red
			self.red, self.green, self.blue = hex_to_rgb(red)
		else:
			self.red = red
			self.green = green
			self.blue = blue
			self.hex = rgb_to_hex(red, green, blue)
	def __repr__(self):
		return self.hex
	def __str__(self):
		return self.hex
	def __eq__(self, other):
		if type(other) == str:
			return self.hex == other
		if type(other) == tuple:
			return (self.red, self.green, self.blue) == other
		if type(other) == list:
			return [self.red, self.green, self.blue] == other
		if type(other) == Colour:
			return self.hex == other.hex
	
def hex_to_rgb(hex):
	hex_decimal_map = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "a": 10, "b": 11, "c": 12, "d": 13, "e": 14, "f": 15}
	red = hex_decimal_map[hex[1]] * 16 + hex_decimal_map[hex[2]]
	green = hex_decimal_map[hex[3]] * 16 + hex_decimal_map[hex[4]]
	blue = hex_decimal_map[hex[5]] * 16 + hex_decimal_map[hex[6]]
	return (red, green, blue)
def rgb_to_hex(red, green, blue):
	decimal_hex_map = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
	red_hex = decimal_hex_map[red // 16] + decimal_hex_map[red % 16]
	green_hex = decimal_hex_map[green // 16] + decimal_hex_map[green % 16]
	blue_hex = decimal_hex_map[blue // 16] + decimal_hex_map[blue % 16]
	return "#" + red_hex + green_hex + blue_hex

WHITE = Colour("#ffffff")
BLACK = Colour("#000000")
BLUE = Colour("#0000ff")
RED = Colour("#ff0000")
GREEN = Colour("#00ff00")
YELLOW = Colour("#ffff00")
CYAN = Colour("#00ffff")
MAGENTA = Colour("#ff00ff")
