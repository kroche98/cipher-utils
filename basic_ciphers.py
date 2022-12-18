import re

NONALPHA_CHARS = re.compile('[^A-Z]')
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ENGLISH_LETTER_FREQS = [
    0.0812, 0.0149, 0.0271, 0.0432, 0.1202, 0.0230, 0.0203, 0.0592, 0.0731, 0.0010, 0.0069, 0.0398, 0.0261,
    0.0695, 0.0768, 0.0182, 0.0011, 0.0602, 0.0628, 0.0910, 0.0288, 0.0111, 0.0209, 0.0017, 0.0211, 0.0007
]

def to_num(c):
    """Convert uppercase character to ordinal number (A = 0, B = 1, etc.)"""
    return ord(c) - 65

def to_chr(n):
    """Convent ordinal number to uppercase character (A = 0, B = 1, etc.)"""
    return chr((n % 26) + 65)

def caesar_encode(msg, shift):
    """Encode given message using Caesar cipher with given shift amount."""

    # first convert to uppercase and remove nonalphabetic chars
    msg = NONALPHA_CHARS.sub('', msg.upper())
    return ''.join(to_chr(to_num(c) + shift) for c in msg)

def caesar_decode(msg, shift):
    """Decode given message using Caesar cipher with given shift amount."""

    # first convert to uppercase and remove nonalphabetic chars
    msg = NONALPHA_CHARS.sub('', msg.upper())
    return ''.join(to_chr(to_num(c) - shift) for c in msg)

def vigenere_encode(msg, key):
    """Encode given message using Vigenere cipher."""

    # first convert to uppercase and remove nonalphabetic chars
    msg = NONALPHA_CHARS.sub('', msg.upper())
    key = NONALPHA_CHARS.sub('', key.upper())
    keylen = len(key)
    return ''.join(to_chr(to_num(msg[i]) + to_num(key[i % keylen])) for i in range(len(msg)))

def vigenere_decode(msg, key):
    """Decode given message using Vigenere cipher."""

    # first convert to uppercase and remove nonalphabetic chars
    msg = NONALPHA_CHARS.sub('', msg.upper())
    key = NONALPHA_CHARS.sub('', key.upper())
    keylen = len(key)
    return ''.join(to_chr(to_num(msg[i]) - to_num(key[i % keylen])) for i in range(len(msg)))

def find_repeats(msg):
    """Find repeated letter sequences in the given message."""
    msg = NONALPHA_CHARS.sub('', msg.upper())
    repeats = {}
    for i in range(len(msg)):
        chunk = msg[i:i+4]
        print(chunk)
        if chunk not in repeats.keys():
            repeats[chunk] = []
        repeats[chunk].append(i)
    return {k:v for k, v in repeats.items() if len(repeats[k]) > 1}

def loss(sample_freqs, offset):
    """Compute loss as mean squared error between message letter
    frequency distribution and English letter frequency distribution.
    """

    return sum(
        (ENGLISH_LETTER_FREQS[j] - sample_freqs[(offset + j) % 26])**2
            for j in range(len(ALPHABET)) )

def find_vigenere_key(msg, keylen):
    """Cracks key of given message encoded with Vigenere cipher.
    
    The length of the key must also be provided.
    """

    key = ''
    for keypos in range(keylen): # find each letter of the key in turn
        sample = msg[keypos::keylen] # slice out all positions with the same shift
        sample_len = len(sample)
        sample_freqs = [sample.count(letter)/sample_len for letter in ALPHABET] # frequencies of A-Z in the message sample
        key_scores = []
        for i in range(len(ALPHABET)): # try all 26 offsets
            key_scores.append(loss(sample_freqs, i))
        best_score = key_scores[0]
        next_key_letter = ALPHABET[0]
        for letter, score in zip(ALPHABET, key_scores):
            if score < best_score:
                best_score = score
                next_key_letter = letter
        key += next_key_letter
    return key

if __name__ == '__main__':
    msg = 'LOMRXLOWINKLLKHJAPJIJLXFKSAQTGSULWXSKQSZGMKTWWTMXLSNMXBKZQRIDLQSMZLMCMJLUJTFKIYMZLAFFWAQRXATXTLKPJQXGMBWTFZTFMAVVZGDLAXMZLSJRAZSSHOUBMXWHAJPAAPBAAJPYAWRMDFSFJJVZHVLXVPAFGGAPJKHVQSMAUNFOGYWKMZLIIHHAQTGGMBMBKJWIXTFBMHKLLJLAYQSZLVBWTFZUNMATXTKLHVYFWZAFZWZENMZVCYMZLAQBYOBJLLKISZWYWKMZLQWFWZAFZWZJJBFNZJTVIGUHDPBNVSSWWUMZQSXKZZNOSSAJMU'
    key = find_vigenere_key(msg, 5)
    print(f'Key: {key}')
    msg_decoded = vigenere_decode(msg, key)
    print(f'Original message: {msg_decoded}')
