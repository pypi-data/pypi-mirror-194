# vitalpy

Welcome to vitalpy - essential tools for programming in Python!

## Installation

Linux / macOS (python3):

``` zsh
python3 -m pip install vitalpy
```

Linux  / macOS (python2):

``` zsh
python -m pip install vitalpy
```

Windows:

``` zsh
py -m pip install vitalpy
```

## Docs

[vitalpy documentation](http://123web.uk/vitalpy/docs)

---

<!--``` python
v.file.ls(path)
```

Returns a list of files in a directory.

Arguments:

* `path`: the folder to search (e.g. `/home/your_name/coding/awesome_project`)

Returns:

`list` of files in the specified directory

``` python
v.file.create(path)
```

---


Creates the specified file.

Arguments:

* `file`: the file to create

Returns:

`list` of files in the specified directory
-->

``` python
v.file.ls(path) #List all files in a folder
v.file.create(file) # Create the specified folder
v.file.write(file, content) # Write some data to a file
v.file.read(file) # Get the contents of a file
v.file.rm(path) # Delete a file
v.file.rmdir(path) # Delete a folder
v.file.mkdir(folder) # Create a folder
v.file.copy(origin, destination) # Copy the origin file to the destination
v.file.append(file, content) # Append the content to the file
v.file.move(origin, destination) # Change the filepath of origin to destination
v.file.rename(origin, destination) # Rename the old_name file to new_name, same as move()
```