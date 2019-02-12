#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import dictLetterFrequency
import dictionary
import math
import sys


def decrypt(cracked_letters, encrypted_text):
    """Returns a decrypted string."""
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
    
    return decrypted_text


# Constants
SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ .'
LETTERS = SYMBOLS[:-2]
DEFAULT_INPUT_FILE_NAME = 'encrypted_book.txt'
DEFAULT_OUTPUT_FILE_NAME = 'decrypted_book.txt'
DICTIONARY = dictionary.words
DICTIONARY_LETTER_TO_OCCURRENCE = dictLetterFrequency.letter_to_occurrence
DICTIONARY_LETTER_TO_OCCURRENCE_TUPLES = sorted(DICTIONARY_LETTER_TO_OCCURRENCE.items(), key=lambda x : x[1], reverse=True)


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

    # Only capture letters A-Z
    if letter in LETTERS:
        if letter in letter_to_occurrence:
            letter_to_occurrence[letter] += 1
        
        else:
            letter_to_occurrence[letter] = 1

letter_occurrence_tuples = sorted(letter_to_occurrence.items(), key=lambda x : x[1], reverse=True)


cracked_letters = {}

# Assume the most frequent letter is space
cracked_letters[letter_occurrence_tuples[0][0]] = ' '


# Decrypt the period char
last_chars_to_occurrence = {}

for word in [s for s in encrypted_text.split('\n\n') if len(s)]:
    char = word[-1].upper()
    if char in SYMBOLS:
        if char in last_chars_to_occurrence:
            last_chars_to_occurrence[char] += 1
        else:
            last_chars_to_occurrence[char] = 1

last_chars_to_occurrence_tuples = sorted(last_chars_to_occurrence.items(), key=lambda x : x[1], reverse=True)

# Assume the period is the most frequently occuring char at the end of paragraphs
cracked_letters[last_chars_to_occurrence_tuples[0][0]] = '.'


# Begin frequency analysis
# Create word pattern for each cipherword in the ciphertext
encrypted_word_patterns = {}
decrypted_text = decrypt(cracked_letters, encrypted_text)
for word in decrypted_text.split():
    pattern = ''
    seen_chars = {}
    count = 0
    for char_index, char in enumerate(word):
        if char_index > 0:
            pattern += '.'

        if not char in seen_chars:
            seen_chars[char] = str(count)
            count += 1

        pattern += seen_chars[char]
    
    encrypted_word_patterns[pattern] = None


# Write decrypted text to output file
with open(output_file_name, 'w') as output_file:
    output_file.write(decrypt(cracked_letters, encrypted_text))
