#!/usr/bin/bash

#Expects a single argument: the filename of the text file to be analyzed.
if [[ $# < 1 ]]; then
   echo "Error: no argument given."
   exit 1
fi
# check existence of file
if [[ !  -e "$1" ]]; then
   echo "Error: file $1 does not exist."
   exit 1
fi

# file exists; we assume that it is readable.

# Now find all the bigrams in the file:
tr -sc '[A-Z][a-z]' '[\012*]' < $1 > ${1}.tr && \
sort ${1}.tr | uniq -c| sort -rg > ${1}.monogram && \
rm ${1}.tr && \
exit 0


# gotten from here: http://www.generation5.org/content/2004/nlpUnix.asp

