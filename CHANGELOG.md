# 📥 Patch Notes:

## Minor Changes:
 - Added `exit` keyword to exit faster (Code 0)
 - Added `license` keyword to view license
 - Modified `exit()` method to include exit codes (0-255)
 - Modified `pass` statement to return NoneType

## Major Changes:
 - Changed Boolean Logic to use Actual Booleans, a subtype of Numbers that can only be 1 or 0
 - Rewrote the Standard Library to be in Python (Grouped into PySTDLIB and CoSTDLIB)
 - Removed `python` module
 - Renamed `fm` -> `fileio`
 - Renamed `str` -> `strutils`
 - Added `listutils`
 - Added Inbuilt Python Libraries of `math`, `time`, `random`, `os` and `sys` to the Standard Library
 - Both `import` and `include` statements have been rewritten, and imports are now recursive

# 🐞 Bug Fixes:
 - Fixed a Bug allowing Keyboard Interrupts to exit a While Loop
 - Fixed a Bug where Lists would not display in the Shell
