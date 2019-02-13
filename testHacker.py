#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import listdir
from os.path import isfile, join
import betterSubCrack as hacker
import simpleSubCipher as sub_cipher

book_file_names = [f for f in listdir('original_books') if isfile(join('original_books', f))]

for file_name in book_file_names:
    with open('original_books/' + file_name, 'r') as book_file:
        book_text = book_file.read()
    
    print(file_name)    

    key = sub_cipher.getRandomKey()
    print('key:', key)
        
    encrypted_text = sub_cipher.encryptMessage(key, book_text)
    
    with open('encrypted_books/' + file_name, 'w') as output_file:
        output_file.write(encrypted_text)

    mapping = hacker.hack(encrypted_text)

    hacked_text = hacker.decrypt_with_cipherletter_mapping(encrypted_text, mapping)
    
    with open('decrypted_books/' + file_name, 'w') as output_file:
        output_file.write(hacked_text)
        
    correct_count = 0
    total = 0
    book_text = book_text.upper()
    hacked_text = hacked_text.upper()
    for i in range(len(book_text)):
        if book_text[i] == hacked_text[i]:
            correct_count += 1
        
        total += 1
    
    print('accuracy:', str(float(correct_count) / total), '\n')
