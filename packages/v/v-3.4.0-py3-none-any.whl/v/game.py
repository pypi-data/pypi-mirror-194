from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

class Window:
	def __init__(self, title, width, height, *, fullscreen=False):
		if fullscreen:
			self.screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
		else:
			self.screen = pygame.display.set_mode((width, height))
