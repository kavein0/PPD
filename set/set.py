import random
import logging
import string
import config as cfg


def set_generator(input_set: str) -> str:
    """
    Generate a password using a custom character set.

    :param input_set: Custom character set or pattern.
    :return: Generated password as a string.
    """

    # Define character sets
    digit_set = string.digits
    lower_set = string.ascii_lowercase
    upper_set = string.ascii_uppercase
    punctuation_set = ',.;:'

    # Log the input set
    logging.debug(f'Input set: {input_set}')

    if '|' in input_set:
        custom_set, exclude_set = input_set.split('|', 1)
        selected_set = random.choice([custom_set, exclude_set])
        input_set = selected_set

    # Handle exclusion of certain symbols from the set
    if '^' in input_set:
        custom_set, exclude_set = input_set.split('^', 1)
        logging.debug(f"Symbols to exclude from set: {exclude_set}")
        cfg.char_set['d'] = ''.join(char for char in digit_set if char not in exclude_set)
        cfg.char_set['l'] = ''.join(char for char in lower_set if char not in exclude_set)
        cfg.char_set['u'] = ''.join(char for char in upper_set if char not in exclude_set)
        cfg.char_set['p'] = ''.join(char for char in punctuation_set if char not in exclude_set)
        input_set = custom_set

    # Generate the set based on the input set
    generated_set = ''

    # Exclude duplicates from input set
    custom_set = set(input_set)

    slash_pattern = False

    for char in custom_set:
        if slash_pattern is True:
            generated_set += char
            logging.debug(f" '{char}' Adding character to template."
                          f"Be careful, using custom char in password can reduce password strength")
            slash_pattern = False
        elif char == '\\':
            slash_pattern = True
            continue
        elif char in cfg.char_set:
            generated_set += cfg.char_set[char]

    # Log the generated set
    logging.debug(f"Final set: {generated_set}")

    return generated_set
