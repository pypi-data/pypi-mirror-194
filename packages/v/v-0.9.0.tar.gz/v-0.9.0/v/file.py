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

def rmdir(path):
	"""Delete a folder"""
	try:
		os.rmdir(path)
		return True
	except Exception as e:
		return e

def mkdir(folder):
	"""Create a folder"""
	try:
		os.mkdir(folder)
		return True
	except Exception as e:
		return e

def copy(origin, destination):
	"""Copy the origin file to the destination"""
	try:
		return shutil.copyfile(origin, destination)
	except Exception as e:
		return e

def append(file, content):
	"""Append the content to the file"""
	try:
		with open(file, "a") as f:
			return f.write(content)
	except Exception as e:
		return e

def move(origin, destination):
	"""Change the filepath of origin to destination"""
	try:
		return shutil.move(origin, destination)
	except Exception as e:
		return e
