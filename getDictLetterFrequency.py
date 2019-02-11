#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dictionary

# Determine the number of occurrences of each letter in the dictionary
letter_to_occurrence = {}
for word in dictionary.words:
    for letter in word:
        if letter in letter_to_occurrence:
            letter_to_occurrence[letter] += 1
        
        else:
            letter_to_occurrence[letter] = 1
            
with open('dictLetterFrequency.py', 'w') as output_file:
    output_file.write('letter_to_occurrence = ' + str(letter_to_occurrence))
