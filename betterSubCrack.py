#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Inspiration: https://www.nostarch.com/crackingcodes

import copy, simpleSubCipher, wordPatterns, makeWordPatterns, sys

# Constants
DEFAULT_INPUT_FILE_NAME = 'encrypted_book.txt'
DEFAULT_OUTPUT_FILE_NAME = 'decrypted_book.txt'
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ .'

def main():
    # Ensure the expected number of command line arguments is provided
    if len(sys.argv) == 3:
        input_file_name = sys.argv[1]
        output_file_name = sys.argv[2]

    else:
        # Incorrect number of command line arguments
        # Use default file names
        input_file_name = DEFAULT_INPUT_FILE_NAME
        output_file_name = DEFAULT_OUTPUT_FILE_NAME

    print('Input file:\t%s\nOutput file:\t%s' % (input_file_name, output_file_name))
        
    # Read the input file
    with open(input_file_name, 'r') as input_file:
        encrypted_text = input_file.read()

    # Determine the possible valid ciphertext translations:
    print('Hacking...')
    letter_mapping = hack(encrypted_text)

    # Display the results to the user:
    print('Mapping:')
    print(letter_mapping)
    print()
    hackedText = decryptWithCipherletterMapping(encrypted_text, letter_mapping)

    # Write decrypted text to output file
    with open(output_file_name, 'w') as output_file:
        output_file.write(hackedText)


def get_blank_cipherletter_mapping():
    """Returns a dictionary of cipherletters to empty lists."""
    mapping = {}
    for char in LETTERS:
        mapping[char] = []
        
    return mapping


def intersect_mappings(mapA, mapB):
    # To intersect two maps, create a blank map, and then add only the
    # potential decryption letters if they exist in BOTH maps.
    intersected_mapping = get_blank_cipherletter_mapping()
    for letter in LETTERS:

        # An empty list means "any letter is possible". In this case just
        # copy the other map entirely.
        if mapA[letter] == []:
            intersected_mapping[letter] = copy.deepcopy(mapB[letter])
        elif mapB[letter] == []:
            intersected_mapping[letter] = copy.deepcopy(mapA[letter])
        else:
            # If a letter in mapA[letter] exists in mapB[letter], add
            # that letter to intersected_mapping[letter].
            for mappedLetter in mapA[letter]:
                if mappedLetter in mapB[letter]:
                    intersected_mapping[letter].append(mappedLetter)

    return intersected_mapping


def consolidate_mapping(letter_mapping):
    # Cipherletters in the mapping that map to only one letter are
    # "solved" and can be removed from the other letters.
    # For example, if 'A' maps to potential letters ['M', 'N'], and 'B'
    # maps to ['N'], then we know that 'B' must map to 'N', so we can
    # remove 'N' from the list of what 'A' could map to. So 'A' then maps
    # to ['M']. Note that now that 'A' maps to only one letter, we can
    # remove 'M' from the list of letters for every other
    # letter. (This is why there is a loop that keeps reducing the map.)

    loop_again = True
    while loop_again:
        # First assume that we will not loop again:
        loop_again = False

        # `solved_letters` will be a list of uppercase letters that have one
        # and only one possible mapping in `letter_mapping`:
        solved_letters = []
        for cipherletter in LETTERS:
            if len(letter_mapping[cipherletter]) == 1:
                solved_letters.append(letter_mapping[cipherletter][0])

        # If a letter is solved, than it cannot possibly be a potential
        # decryption letter for a different ciphertext letter, so we
        # should remove it from those other lists:
        for cipherletter in LETTERS:
            for s in solved_letters:
                if len(letter_mapping[cipherletter]) != 1 and s in letter_mapping[cipherletter]:
                    letter_mapping[cipherletter].remove(s)
                    if len(letter_mapping[cipherletter]) == 1:
                        # A new letter is now solved, so loop again.
                        loop_again = True

    return letter_mapping, solved_letters


def hack(encrypted_text):
    # Determine the number of occurrences of each letter in the encrypted text
    letter_occurrences = {}
    for letter in encrypted_text:
        letter = letter.upper()

        if letter in LETTERS:
            if letter in letter_occurrences:
                letter_occurrences[letter] += 1
            
            else:
                letter_occurrences[letter] = 1

    # Assume the most frequent letter is space and get the encrypted char
    encrypted_space = sorted(letter_occurrences.items(), key=lambda x : x[1], reverse=True)[0][0]

    # Determine the most frequent end-of-paragraph character
    last_char_occurrences = {}
    for word in [s for s in encrypted_text.split('\n\n') if len(s)]:
        char = word[-1].upper()
        if char.upper() in LETTERS:
            if char in last_char_occurrences:
                last_char_occurrences[char] += 1
            else:
                last_char_occurrences[char] = 1

    # Assume the period is the most frequently occuring char at the end of paragraphs
    encrypted_period = sorted(last_char_occurrences.items(), key=lambda x : x[1], reverse=True)[0][0]
    
    # Save a copy of the encrypted text with no encrypted periods (for easier cracking later)
    encrypted_text_copy = encrypted_text.replace(encrypted_period.lower(), '').replace(encrypted_period, '')

    # Get a fresh mapping to populate
    cipherletter_map = get_blank_cipherletter_mapping()
    
    # Fill in the mapping with known encryptions
    cipherletter_map[encrypted_period] = ['.']
    cipherletter_map[encrypted_space] = [' '] 

    # Clean up the ciphertext for easier cracking
    ciphertext = ''.join([c.upper() for c in encrypted_text_copy if c.upper() in LETTERS])
    cipherword_list = [s for s in ciphertext.split(encrypted_space) if len(s)]

    for cipherword in cipherword_list:
        # Get a new cipherletter mapping for each ciphertext word:
        candidateMap = get_blank_cipherletter_mapping()

        wordPattern = makeWordPatterns.getWordPattern(cipherword)
        if wordPattern not in wordPatterns.allPatterns:
            continue # This word was not in our dictionary, so continue.

        # Add the letters of each candidate to the mapping:
        for candidate in wordPatterns.allPatterns[wordPattern]:
            for i in range(len(cipherword)):
                if candidate[i] not in candidateMap[cipherword[i]]:
                    candidateMap[cipherword[i]].append(candidate[i])

        # Intersect the new mapping with the existing intersected mapping:
        cipherletter_map = intersect_mappings(cipherletter_map, candidateMap)
        
        cipherletter_map, solved_letters = consolidate_mapping(cipherletter_map)
        
        if len(LETTERS) == len(solved_letters):
            # A valid mapping has been found
            break

    return cipherletter_map


def decryptWithCipherletterMapping(ciphertext, letter_mapping):
    # Return a string of the ciphertext decrypted with the letter mapping,
    # with any ambiguous decrypted letters replaced with an _ underscore.

    # First create a simple sub key from the letter_mapping mapping:
    key = ['x'] * len(LETTERS)
    for cipherletter in LETTERS:
        if len(letter_mapping[cipherletter]) == 1:
            # If there's only one letter, add it to the key.
            keyIndex = LETTERS.find(letter_mapping[cipherletter][0])
            key[keyIndex] = cipherletter
        else:
            ciphertext = ciphertext.replace(cipherletter.lower(), '_')
            ciphertext = ciphertext.replace(cipherletter.upper(), '_')
    key = ''.join(key)

    # With the key we've created, decrypt the ciphertext:
    return simpleSubCipher.decryptMessage(key, ciphertext)


if __name__ == '__main__':
    main()
