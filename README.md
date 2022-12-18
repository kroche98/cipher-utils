# Cipher Utils

Simple functions for working with Caesar and Vigenere ciphers.

Includes functions to encode and decode Caesar and Vigenere.

Also includes function to crack Vigenere cipher (and by extension Caesar, which is just a Vigenere with key length 1). It does this by computing for each letter of the key the mean squared error between the letter frequency distributions of the associated ciphertext and of typical English text.

Also includes a sample (not cryptographically secure) implementation of the knapsack cipher.
