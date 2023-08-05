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
			