import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os"],
    "includes": ["ConfigParser"],
    "excludes": ["tkinter"],
    "include_files": ["dgmeffects.json","dgmexpressions.json"]
}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Expression Tree GUI",
        version = "0.1",
        description = "GUI frontend for browsing EVE Online effect expression trees",
        options = {"build_exe": build_exe_options},
        executables = [Executable("exp_gui.py", base=base)])
