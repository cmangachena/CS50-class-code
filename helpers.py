
\
from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""
    a = set(a.split("\n"))
    b = set(b.split("\n"))
    matches = a.intersection(b)
    return matches


def sentences(a, b):
    """Return sentences in both a and b"""
    a = set(sent_tokenize(a))
    b = set(sent_tokenize(b))

    matches2 = a.intersection(b)
    return matches2


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    file1_set=set()
    file2_set = set()

    for i in range (len(a) - n + 1):
        file1_set.add(a[i : i+n])

    for j in range (len(b) - n + 1):
        file2_set.add(b[j : j+n])

    a = set(file1_set)
    b = set(file2_set)

    matches3 = a.intersection(b)
    return matches3
