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

def rgb_to_hex(red, green, blue):
	decimal_hex_map = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
	red_hex = decimal_hex_map[red // 16] + decimal_hex_map[red % 16]
	green_hex = decimal_hex_map[green // 16] + decimal_hex_map[green % 16]
	blue_hex = decimal_hex_map[blue // 16] + decimal_hex_map[blue % 16]
	return "#" + red_hex + green_hex + blue_hex