#!/usr/bin/bash

#Expects first argument: the filename of the text file to be analyzed.
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

if [[ $2 -le 0 ]]; then
   echo "Error: n must be positive."
   exit 1
fi

# Now find all the ngrams in the file.
# convert to lower case:
tr '[:upper:]' '[:lower:]' < $1 > ${1}.lc
# use tr to isolate words on their own line:
tr -sc '[A-Z][a-z]' '[\012*]' < ${1}.lc > ${1}.tr

# isolate parts of n-grams in separate files
for (( i=1; i <= $2; i++)); do
   echo "tailing ${i}..."
   tail -n +${i} ${1}.tr > ${1}.${i}part
done

# consolidate parts of ngrams into one file, of all ngrams
echo "" > ${1}.intermediate
touch ${1}.cp
for ((i=1; i <= $2; i++)); do
   echo "pasting ${i}..."
   #paste combines corresponding lines of two or more files
   paste ${1}.intermediate ${1}.${i}part > ${1}.cp
   cp ${1}.cp ${1}.intermediate
done

# ${1}.intermediate
# sort the ngrams, count the unique occurrences, sort in descending order
echo "sorting and counting uniques"
sort ${1}.intermediate| uniq -c| sort -rg > ${1}.${2}gram

#cleanup
rm ${1}.lc
rm ${1}.tr
for ((i=1; i <= $2; i++)); do
   rm ${1}.${i}part
done
rm ${1}.cp
rm ${1}.intermediate
exit 0


# gotten from here: http://www.generation5.org/content/2004/nlpUnix.asp

