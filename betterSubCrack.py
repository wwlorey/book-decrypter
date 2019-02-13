#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Inspiration: https://www.nostarch.com/crackingcodes

import copy, simpleSubCipher, wordPatterns, makeWordPatterns, sys, re

# Constants
DEFAULT_INPUT_FILE_NAME = 'encrypted_book.txt'
DEFAULT_OUTPUT_FILE_NAME = 'decrypted_book.txt'
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ .'
NON_LETTERS_PATTERN = re.compile('[^A-Z\. ]')

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

    # Hack
    print('Hacking...')
    letter_mapping = hack(encrypted_text)

    # Display resulting map
    print('Mapping:')
    print(letter_mapping)
    print()
    hacked_text = decrypt_with_cipherletter_mapping(encrypted_text, letter_mapping)

    # Write decrypted text to output file
    with open(output_file_name, 'w') as output_file:
        output_file.write(hacked_text)


def get_blank_cipherletter_mapping():
    """Returns a dictionary of cipherletters to empty lists."""
    mapping = {}
    for char in LETTERS:
        mapping[char] = []
        
    return mapping


def intersect_mappings(mapA, mapB):
    """Returns the intersection of mapA and mapB."""
    intersected_mapping = get_blank_cipherletter_mapping()

    for letter in LETTERS:
        if mapA[letter] == []:
            intersected_mapping[letter] = copy.deepcopy(mapB[letter])

        elif mapB[letter] == []:
            intersected_mapping[letter] = copy.deepcopy(mapA[letter])

        else:
            for mappedLetter in mapA[letter]:
                if mappedLetter in mapB[letter]:
                    intersected_mapping[letter].append(mappedLetter)

    return intersected_mapping


def consolidate_mapping(letter_mapping):
    """Removes letters from letter_mapping that have been solved, returning
    letter_mapping. Also returned is the list of solved letters.
    """
    loop_again = True

    while loop_again:
        loop_again = False

        solved_letters = []
        for cipherletter in LETTERS:
            if len(letter_mapping[cipherletter]) == 1:
                solved_letters.append(letter_mapping[cipherletter][0])

        for cipherletter in LETTERS:
            for s in solved_letters:
                if len(letter_mapping[cipherletter]) != 1 and s in letter_mapping[cipherletter]:
                    letter_mapping[cipherletter].remove(s)
                    if len(letter_mapping[cipherletter]) == 1:
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
    
    # Get a fresh mapping to populate
    cipherletter_map = get_blank_cipherletter_mapping()
    
    # Fill in the mapping with known encryptions
    cipherletter_map[encrypted_period] = ['.']
    cipherletter_map[encrypted_space] = [' '] 

    # Clean up the ciphertext for easier cracking
    cipherword_list = [s for s in NON_LETTERS_PATTERN.sub(encrypted_space, encrypted_text.upper()).replace(encrypted_period, '').split(encrypted_space) if s]
    
    for cipherword in cipherword_list:
        candidateMap = get_blank_cipherletter_mapping()

        wordPattern = makeWordPatterns.getWordPattern(cipherword)
        if wordPattern not in wordPatterns.allPatterns:
            continue

        # Add the letters of each candidate to the mapping
        for candidate in wordPatterns.allPatterns[wordPattern]:
            for i in range(len(cipherword)):
                if candidate[i] not in candidateMap[cipherword[i]]:
                    candidateMap[cipherword[i]].append(candidate[i])

        cipherletter_map = intersect_mappings(cipherletter_map, candidateMap)
        
        cipherletter_map, solved_letters = consolidate_mapping(cipherletter_map)
        
        if len(LETTERS) == len(solved_letters):
            # A valid mapping has been found
            break

    return cipherletter_map


def decrypt_with_cipherletter_mapping(ciphertext, letter_mapping):
    """Returns the resulting string decrypted using letter_mapping
    on ciphertext.
    """
    key = ['x'] * len(LETTERS)
    for cipherletter in LETTERS:
        if len(letter_mapping[cipherletter]) == 1:
            key_index = LETTERS.find(letter_mapping[cipherletter][0])
            key[key_index] = cipherletter
        else:
            ciphertext = ciphertext.replace(cipherletter.lower(), '_')
            ciphertext = ciphertext.replace(cipherletter.upper(), '_')
    key = ''.join(key)

    return simpleSubCipher.decryptMessage(key, ciphertext)


if __name__ == '__main__':
    main()
