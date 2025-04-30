import string
'''
Config module consist of characters_set that will 
be used in password generation
'''
char_set = {
    'd': string.digits,
    'l': string.ascii_lowercase,
    'u': string.ascii_uppercase,
    'p': ',.;:',
    'a': string.ascii_lowercase + string.digits,
    'A': string.ascii_uppercase + string.ascii_lowercase + string.digits,
    'U': string.ascii_uppercase + string.digits,
    'h': string.hexdigits.lower(),
    'H': string.hexdigits.upper(),
    'v': 'aeiou',
    'V': 'AEIOUaeiou',
    'b': '(){}[]<>',
    'Z': 'AEIOU',
    'c': 'bcdfghjklmnpqrstvwxyz',
    'C': 'bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXY',
    'z': 'BCDFGHJKLMNPQRSTVWXYZ',
    'S': string.printable,
    's': string.punctuation,
    'x': ''.join([chr(i) for i in range(0xA1, 0xAD)] + [chr(i) for i in range(0xAE, 0xFF + 1)])
}
