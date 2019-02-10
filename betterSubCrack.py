#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dictionary
import sys

# Constants
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ .'
DEFAULT_INPUT_FILE_NAME = 'encrypted_book.txt'
DEFAULT_OUTPUT_FILE_NAME = 'decrypted_book.txt'
DICTIONARY = dictionary.words

# Ensure the expected number of command line arguments is provided
if len(sys.argv) == 3:
    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]

else:
    # Incorrect number of command line arguments
    # Use default file names
    input_file_name = DEFAULT_INPUT_FILE_NAME
    output_file_name = DEFAULT_OUTPUT_FILE_NAME

print('Input file: %s\nOutput file: %s' % (input_file_name, output_file_name))
    
# Read the input file
with open(input_file_name, 'r') as input_file:
    encrypted_text = input_file.read()

# Determine the number of occurrences of each letter in the encrypted text
letter_to_occurrence = {}
for letter in encrypted_text:
    letter = letter.upper()

    if letter in LETTERS:
        if letter in letter_to_occurrence:
            letter_to_occurrence[letter] += 1
        
        else:
            letter_to_occurrence[letter] = 1

letter_occurrence_tuples = sorted(letter_to_occurrence.items(), key=lambda x : x[1], reverse=True)

# Assume the most frequent letter is space
space_tuple = letter_occurrence_tuples.pop(0)
cracked_letters = {}
cracked_letters[space_tuple[0]] = ' '

# Decrypt the book
decrypted_text = ''

for letter in encrypted_text:
    if letter.upper() in cracked_letters:
        # This letter has been cracked
        # Ensure it decrypts with the correct case
        if letter.isupper():
            decrypted_text += cracked_letters[letter.upper()].upper()
        
        else:
            decrypted_text += cracked_letters[letter.upper()].lower()

    else:
        # This letter is not in the symbol set or it has not yet been cracked
        decrypted_text += letter

# Write decrypted text to output file
with open(output_file_name, 'w') as output_file:
    output_file.write(decrypted_text)
