# 📥 Patch Notes:

## Minor Changes:
 - Added `exit` keyword to exit faster (Code 0)
 - Added `license` keyword to view license
 - Modified `exit()` method to include exit codes (0-255)
 - Modified `pass` statement to return NoneType
 - Renamed `fm` -> `fileio`
 - Renamed `str` -> `strutils`
 - Added Dev Utilities activated from changing the `MODE` Constant in the `Data.py` file to 0
     - Displays Lexer using `pprint` and the Pretty Print feature
     - Displays AST

## Major Changes:
 - Changed Boolean Logic to use the `Bool` type, a subtype of Numbers that can only be 1 or 0 (a.k.a. `True` and `False`)
 - Rewrote the Standard Library to be in Python (Grouped into PySTDLIB and CoSTDLIB)
 - Removed `python` module
 - Added `listutils`
 - Added Inbuilt Python Libraries of `math`, `time`, `random`, `os`, `sys`, `json` and `re` to the Standard Library
 - Both `import` and `include` statements have been rewritten, and imports are now recursive

# 🐞 Bug Fixes:
 - Fixed a Bug allowing Keyboard Interrupts to exit a While Loop
 - Fixed a Bug where Lists would not display in the Shell
 - Fixed a Bug where Comments would exit in the Shell
 - Fixed a Bug where Keyboard Interrupts would print out lots of empty lines
 - Fixed a Bug where Comments could not be on the same line as other pieces of code

## 🚧 Behind the Scenes:
 - Comments are now processed as their own tokens and are processed as PassNodes by the AST
 - `COMMENT` tokens have `NEWLINE` Buffers on Both Sides
 - Python Objects are now wrapped in Nytescript (Refer to `PyObject`)
