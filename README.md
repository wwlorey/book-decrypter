# pa01 - Name the book: Write a crack for an improved substitution encryption

## Assignment description
The encrypted_book.txt has been encrypted with a more effective version of the substitution cipher which also encrypts spaces and more.
This improved cipher is given to you (the enemy knows the system) in the `simpleSubCipher.py`
Your job is to write a python script which will crack this encryption in the general case.
You will probably want some kind of frequency or transitional probability methods.

1. From scratch, write a python3 script called `betterSubCrack.py`

2. We will execute your script as follows:

    `$ ./betterSubCrack.py name_of_file_to_crack.txt decrypted_file_to_write.txt`

    hint: you will need to add at least file input/output, command line arguments, a change of the permissions of the crack script, and a shebang.

3. It must run in under 2 minutes (or so).

4. You should test encrypting other examples from https://www.gutenberg.org/ebooks/ and then cracking them, to verify that your program can produce correct decryptions.

5. It must run in python3 in the latest up-to-date stable Debian VM, where we will do all grading. 

6. All files must be utf-8 unix delimted.

## Tips and tricks
* What is the most frequent character?
* What is the pattern for a full-stop '.' ?
* How many letters would you match with nothing but a pure letter frequency analysis?
* Careful with the headers! 
* Test with know encryptions (books you encrypt using the included source code).

## Note (actually do this)!!
Thoroughly read the syllabus sections on "Programming assignments" and "Grading". These sections give good tips, tricks, hints, and instructions for programming assignments, including how to submit via Git.

## Grading
It does not need to be perfect; we will give you a % accuracy score. 
Specifically, if you got 99% of the characters in the book, you would receive 99% of the below points.
To be generous with points, this won't be linear, but more in your favor, where cracking 70% of letters would be better than a 70.

95% of this assignment will be graded based on the successful implementation of the crack and correct output.
A fully correct submission will result in a grade of 95%.
The remaining 5% will be awarded based on run-time for you main, with the student with the fastest run-time in the class receiving a 100%, and the slowest correct submission receiving 95%, and a linear interpolation (not sequential) using your actual time in between.
Time tests will be averaged over many book-encryption cracks for accuracy with students always compared on the same machine/environment.

## Re-grades and late work
As with all assignments.

## Due date
Please see the schedule for all due dates.

