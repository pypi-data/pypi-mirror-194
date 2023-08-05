import os, shutil

def ls(path):
	"""List all files in a folder"""
	try:
		return os.listdir(path)
	except Exception as e:
		return e

def create(file):
	"""Create the specified folder"""
	try:
		return open(file, "x")
	except Exception as e:
		return e

def read(file):
	"""Get the contents of a file"""
	try:
		with open(file):
			return file.read()
	except Exception as e:
		return e

def rm(path):
	"""Delete a file"""
	try:
		os.remove(path)
		return True
	except Exception as e:
		return e
