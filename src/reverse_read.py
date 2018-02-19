# This python script finds the reverse read file for a FASTQ forward read

import fnmatch, os

def match(file,string):
 if fnmatch.fnmatch(file,string): match = True
 else: match = False
 return(match)

def match_case(letter,comparison):
 letter = comparison
 return(letter)

def find(sample_name,files):
# Finds the reverse read FASTQ companion for 'forward_read'
 reverse_read_file = ""
 for file in files:
  for letter in file:
   if reverse_read_file == "":
    reverse_read_file = match_case(letter,file.split(letter,1)[0])
   else:
    if letter == any(["-","_"]):
     reverse_read_file = reverse_read_file+letter
     break
    match_string = reverse_read_file.split(letter,2)[0]
    print(match_string)
    if match_case(file,match_string) == match_string: 
     reverse_read_file = reverse_read_file+letter
     break
    else:
     if letter.upper() != letter: letter = letter.upper()
     else: letter = letter.lower()
     if match(file,file.split(letter,1)[0]): 
      reverse_read_file = reverse_read_file+letter
     else: break
  if "FASTQ" in reverse_read_file: break
# print(reverse_read_file)
 return(reverse_read_file)