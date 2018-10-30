import sys
from cs50 import get_string
from sys import argv

# Check if user input is correct
if len(sys.argv) != 2:
    print("Usage: python caesar.py key")
    exit(1)
try:
    key = int(argv[1])
except:
    print("Usage: python caesar.py key")
    exit(1)
# Get message to be encrypted from user
plaintext = get_string("Plaintext: ")

# Encrypt plain text
plaintext_list = []
for ch in plaintext:
    ascii_plaintext = ord(ch)
    plaintext_list.append(ascii_plaintext)
# Add key
ciphertext_list = []
for i in plaintext_list:
    if i in range(65, 97):
        k = (((i-65+key) % 26)+65)
        ciphertext_list.append(k)
    elif i in range(97, 122):
        j = (((i-97 + key) % 26)+97)
        ciphertext_list.append(j)
    else:
        ciphertext_list.append(i)
ciphertext_charlist = []
for i in ciphertext_list:
    char_ciphertext = chr(i)
    ciphertext_charlist.append(char_ciphertext)
print("ciphertext: ", end="")
# Print cipgertext
print("".join(ciphertext_charlist))
