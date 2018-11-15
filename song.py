def main():
    sing()


def sing():
    #Make loop not recursive
    while True:
        print("This is the song that doesn't end.")
        print("Yes, it goes on and on my friend.")
        print("Some people started singing it not knowing what it was,")
        print("And they'll continue singing it forever just because...")
        sing()


if __name__ == "__main__":
    main()