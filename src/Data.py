#######################################
# INTERNAL IMPORTS
#######################################

import string
import os, sys
import importlib

#######################################
# CONSTANTS
#######################################

DIGITS = '0123456789'
LETTERS = string.ascii_letters + '_'
LETTERS_DIGITS = LETTERS + DIGITS
VERSION = '0.8.7'
FILE_EXTENSION = '.ns'
LICENSE = """
MIT License

Copyright (c) 2025 0xnCubed and David Callanan

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
    "math":   ("module", "math"),
    "random": ("module", "random"),
	"time":   ("module", "time"),
	"os":     ("module", "os"),
	"sys":    ("module", "sys"),

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

info = "strutils: A simple string utility module."
"""),
	"listutils": ("code", """
def starmap(func, lst):
	return [func(x) for x in lst]
			   
def filter(func, lst):
	return [x for x in lst if func(x)]

def sort(lst, key=None, reverse=False):
	return sorted(lst, key=key, reverse=reverse)
			   
info = "listutils: A simple list utility module."
"""),
	"fileio": ("code", """
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
			
info = "fileio: A simple file I/O module using Object-Oriented Programming."
"""),
}