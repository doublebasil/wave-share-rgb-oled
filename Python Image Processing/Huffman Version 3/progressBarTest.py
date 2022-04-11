from time import sleep as s
import sys
for i in range(0, 30):
    mystring = ("#" * i) + "\r"
    sys.stdout.write(mystring)
    s(0.1)