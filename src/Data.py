#######################################
# INTERNAL IMPORTS
#######################################

import string
import os, sys, platform
import importlib
from pprint import pp
from functools import lru_cache

#######################################
# CONSTANTS
#######################################

DIGITS = '0123456789'
LETTERS = string.ascii_letters + '_'
LETTERS_DIGITS = LETTERS + DIGITS
VERSION = '0.8.8'
FILE_EXTENSION = '.ns'
MODE = 1
LICENSE = """
MIT License

Copyright (c) 2025-2026 0xnCubed and David Callanan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

#######################################
# STDLIB
#######################################

STDLIB = {
    # Type 1: Inbuilt Python Modules
    "math":     ("module", "math"),
    "random":   ("module", "random"),
	"time":     ("module", "time"),
	"os":       ("module", "os"),
	"sys":      ("module", "sys"),
	"json":     ("module", "json"),
	"re":       ("module", "re"),
	"platform": ("module", "platform"),

    # Type 2: Coded Python Modules
    "strutils": ("code", """
def upper(s):
    return s.upper()

def lower(s):
    return s.lower()

def split(s, sep=None):
	return s.split(sep)

def cutprefix(s, prefix):
	return s.removeprefix(prefix)

def cutsuffix(s, suffix):
	return s.removesuffix(suffix)
				 
def join(lst, s=''):
	return s.join(lst)

def replace(s, sub):
	return s.replace(*sub)

info = "strutils: A simple string utility module."
"""),
	"listutils": ("code", """
def starmap(func, lst):
	return [func(x) for x in lst]
			   
def filter(func, lst):
	return [x for x in lst if func(x)]

def sort(lst, key=None, reverse=False):
	return sorted(lst, key=key, reverse=reverse)
			   
def count(lst, item):
	return lst.count(item)
			   
def slice(lst, start, end=None, step=1):
	if end != None:
		return lst[start:end:step]
	else:
		return lst[start::step]
			   
info = "listutils: A simple list utility module."
"""),
	"fileio": ("code", """
import os
class File:
	def __init__(self, filename, mode='r'):
		self.filename = filename
		self.mode = mode
		self.file = open(filename, mode)
	def read(self):
		return self.file.read()
	def write(self, data):
		if mode != 'w' and mode != 'a':
			raise Exception("File not opened in write or append mode")
		self.file.write(data)
	def close(self):
		self.file.close()
	def __repr__(self):
		return f"<File at {self.filename} on {self.mode} Mode>"

def exists(filename):
	return os.path.exists(filename)

def remove(filename):
	os.remove(filename)			
info = "fileio: A simple file I/O module using Object-Oriented Programming."
"""),
	"py": ("code", """
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
def exect(codesnippet):
	return exec(codesnippet)

def create_window(title="EasyTk Window", size="800x600", resizable=(True, True)):
    \"\"\"
    Initializes the main application window.
    Returns: The root window object.
    \"\"\"
    root = tk.Tk()
    root.title(title)
    root.geometry(size)
    root.resizable(resizable[0], resizable[1])
    return root

def create_container(parent, side="top", fill="both", expand=True, padding=10, horizontal=False):
    \"\"\"
    Creates a Frame (container) to organize other widgets.
    \"\"\"
    frame = ttk.Frame(parent, padding=padding)
    frame.pack(side=side, fill=fill, expand=expand)
    return frame

def add_label(parent, text, font=("Arial", 12), color=None, pady=5):
    \"\"\"
    Adds a text label to the parent container.
    "\"\"\""
    label = ttk.Label(parent, text=text, font=font)
    if color:
        label.configure(foreground=color)
    label.pack(pady=pady)
    return label

def add_button(parent, text, command, style=None, pady=5):
    \"\"\"
    Adds a clickable button.
    \"\"\"
    button = ttk.Button(parent, text=text, command=command)
    button.pack(pady=pady)
    return button

def add_input(parent, default_text="", width=30, pady=5, password=False):
    \"\"\"
    Adds a text entry field. 
    Returns: The Entry widget (use .get() to retrieve text).
    "\"\"\""
    show = "*" if password else ""
    entry = ttk.Entry(parent, width=width, show=show)
    entry.insert(0, default_text)
    entry.pack(pady=pady)
    return entry

def add_checkbox(parent, text):
    \"\"\"
    Adds a checkbox.
    Returns: (The BooleanVar tracking state, The Checkbutton widget).
    "\"\"\""
    var = tk.BooleanVar()
    cb = ttk.Checkbutton(parent, text=text, variable=var)
    cb.pack(pady=5)
    return var, cb

def show_message(title, message, type="info"):
    \"\"\"
    Wrapper for standard dialog boxes.
    Types: info, warning, error
    \"\"\"
    if type == "info":
        messagebox.showinfo(title, message)
    elif type == "warning":
        messagebox.showwarning(title, message)
    elif type == "error":
        messagebox.showerror(title, message)

def run_app(root):
    \"\"\"
    Starts the Tkinter main loop.
    \"\"\"
    root.mainloop()		

info = "py: A minimal module to run Python Code through functions."
"""),
	"typelib": ("code", """
# To be thought through
info = "typelib: A simple module to do type checking and advanced manipulation."
"""),
}