import sys
import os

print("Hello stdout")
print("Hello stderr", file=sys.stderr)

with open("debug_output.txt", "w") as f:
    f.write("Python is working\n")
    f.write(f"CWD: {os.getcwd()}\n")
