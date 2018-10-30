from cs50 import get_int

# Get input from user
n = get_int("Height of pyramid: ")
# Check input from user
while n < 1 or n > 9:

    n = get_int("Height of pyramid: ")
    print("", n)

# Print hashes such that you have spaces and hashes that form a pyramids.
for i in range(n):
    for k in range(n-1-i):
        print(" ", end="")

    for j in range(i+1):
        print("#", end="")
    print()