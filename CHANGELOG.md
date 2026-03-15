# 📥 Patch Notes:
- Added Tuples (Same format as Python)
- Changed String, List and Tuple Slicing to Use a Dynamic Tuple system (1 item for Indexing, 2 items for Start, End, 3 items for Start, End, Step)
- Slicing can use NoneType for Default Values (Beginning, End, 1)
- Changed Shell Output Format for Entries with Multiple Statements (Line by line instead of all at once
- Allow Recursive Dot Notation `sys.stdin.read()` without needing parentheses for Ordering `(sys.stdin).read()`
- Added `platform` to STDLIB
- Added `py` module to STDLIB with an `exect()` to run any python code

# 🐞 Bug Fixes:
- Fixed Recursive Module Import Value Wrapping (Fixed to Linear vs Recursive)
- Fixed Recursive STDLIB Import Bug
