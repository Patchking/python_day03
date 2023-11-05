import sys, string
from random import choices

with open("peoples", "w") as file:
    for i in range(int(sys.argv[1]) - 3):
        file.write(''.join(choices(string.digits, k = 10)) + "\n")
    for i in range(3):
        file.write(str(i + 1) * 10 + "\n")
    

    