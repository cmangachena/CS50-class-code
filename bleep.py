import sys
from cs50 import get_string
from sys import argv


def main():

    if len(sys.argv) != 2:
        print("Usage: python bleep.py banned.txt")
        exit(1)

    # Open text file from comand line (from Stack Overflow)
    with open(argv[1], 'r') as f:
        str = f.read()
    # To remove any attached new lines and split string
    banned_stripped = (str.strip())
    banned_split = banned_stripped.split()

    # Create set
    banned_set = set(banned_split)

    # Prompt user to provide message
    message = get_string("What message would you like to censor?" '\n')

    # Check for membership of banned word in set
    message_stripped = message.strip()

    # Remove any attached new lines
    message_word = message_stripped.split()

    # Check if word in message is banned and print censored message
    for i in message_word:
        j = i.lower()
        if j in banned_set:
            print(len(j)*"*", end=" ")
        elif j not in banned_set:
            print(i, end=" ")
    print()


if __name__ == "__main__":
    main()

