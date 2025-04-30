import random
import re
import logging
from set.set import set_generator
import config as cfg


def handle_custom_set(match: re.Match) -> str:
    """
    Handle custom characters in the template.

    :param match: Match object containing the escape character.
    :return: The escaped character.
    """
    custom_set = set_generator(match.group(1))
    logging.warning("Be careful, using custom set in password can reduce password strength")
    logging.debug(f"Using custom set {custom_set}")
    custom_set = ''.join(random.choices(custom_set, k=len(match.group(1))))
    return custom_set


def check_template(template: str) -> str:
    """
    Generate a password based on a template.

    :param template: Template string defining the password layout.
    :return: Generated password as a string.
    """

    # Initialize password
    password = ''

    # Compile regex patterns
    custom_set_pattern = re.compile(r'\[(.*?)\]')
    repeat_pattern = re.compile(r'\{(\d+)\}')

    # Function to handle repeat placeholders
    def repeat_placeholders(match):
        pattern = ''
        repeat_count = int(match.group(1))
        if re.findall(custom_set_pattern, template):

            # Find all substrings inside square brackets and join them into a single string
            substrings = set_generator(''.join(re.findall(r'\[(.*?)\]', template)))
            # Use random.choices to select characters from the combined substrings
            pattern = ''.join(random.choices(substrings, k=repeat_count))

        else:
            previous_char = template[match.start() - 1]
            for _ in range(repeat_count):
                pattern += previous_char
            logging.debug(f"Multiply {previous_char} {repeat_count} times")
        return pattern

    # Handle repeat placeholders in the template
    if re.findall(repeat_pattern, template):
        temp = repeat_placeholders(repeat_pattern.search(template))
        password += temp
        template = ''.join(char for char in temp if char not in template)
    elif re.findall(custom_set_pattern, template):
        temp = custom_set_pattern.sub(handle_custom_set, template)
        password += temp
        template = ''.join(char for char in temp if char not in template)

    slash_pattern = False
    # Generate the password based on the template
    for char in template:
        if slash_pattern is True:
            password += char
            logging.debug(f" '{char}' Adding character to template."
                          f"Be careful, using custom char in password can reduce password strength")
            slash_pattern = False
        elif char == '\\':
            slash_pattern = True
            continue
        elif char in cfg.char_set:
            password += random.choice(cfg.char_set[char])
            logging.debug(f"Add char {char} to password")
        else:
            logging.warning(f"Undefined character in template: {char}")
    return password
