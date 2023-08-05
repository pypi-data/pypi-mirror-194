import os, shutil

def ls(path):
	"""List all files in a folder"""
	try:
		return os.listdir(path)
	except Exception as e:
		return e

