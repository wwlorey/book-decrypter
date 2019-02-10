#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

# Constants
DEFAULT_INPUT_FILE_NAME = 'encrypted_book.txt'
DEFAULT_OUTPUT_FILE_NAME = 'decrypted_book.txt'

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
