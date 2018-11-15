import sys
from cs50 import get_string


def main():

    # Ensure proper usage
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        exit("Usage: python slanted.py depth")
    depth = int(sys.argv[1])

    # Encrypt message
    message = get_string("Message: ")
    if len(message) >= depth:
        print("Slanted:", slant(message, depth))


def slant(message, depth):

    #TODO


if __name__ == "__main__":
    main()
