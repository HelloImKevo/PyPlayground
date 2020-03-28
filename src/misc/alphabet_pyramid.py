# Alphabet pyramid!
# -------------------------------------------------------------------

import time

k = 0

rows = 14

char = chr(65)

# -------------------------------------------------------------------

for i in range(1, rows + 1):
    for space in range(1, (rows - i) + 1):
        print(end=" ")
    while k != ((2 * i) - 1):
        print(("%s " % char), end="")
        time.sleep(0.05)
        k = k + 1
        char = ord(char) + 1
        char = chr(char)
    char = chr(65)
    k = 1
    print()
