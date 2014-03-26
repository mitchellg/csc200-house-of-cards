#!/usr/bin/env python2.7
import codecs
import sys
from nltk import bigrams

# Have to have NTLK installed (with python 2.7): http://www.nltk.org/install.html
# Creates a file where each line represents a bigram in the original text; does not filter duplicates.

def gen_bigrams(text):
    textbig = codecs.open(text, 'r','utf8').read()
    tokens = textbig.split()
    bigram = bigrams(tokens)
    out = codecs.open("{}_bigram.txt".format(text), 'w', 'utf8')
    for ml in bigram:
        out.write(" ".join(ml))
        out.write("\n")

def main():
    inp = sys.argv[1]
    gen_bigrams(inp)

main()
