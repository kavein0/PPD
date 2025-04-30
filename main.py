import argparse
import random
import string
import logging

from template.template import check_template
from set.set import set_generator
from loggin.setup_loggin import setup_logging

# Error to handle argument mistake
ERROR_BAD_OPTION = 1

# Error to handle FILE_NOT_FOUND
FILE_NOT_FOUND = 2

# Error to handle PERMISSION_DENIED
PERMISSION_DENIED = 157


def generate_password(length: int, template: str = None, character_set: str = None) -> str:
    """
    Generate a password based on the provided parameters.

    :param length: Length of the password to be generated.
    :param template: Template string for the password.
    :param character_set: Custom character set to use for password generation.
    :return: Generated password as a string.
    """

    password = ''

    if length is None:
        logging.warning('Length is not provided use default value 9.')
        length = 9

    # If no character set or template is provided, use a default set
    if character_set is None and template is None:
        logging.debug(f"Using default mod for password.")
        password_set = string.ascii_letters + string.digits + string.punctuation
        logging.debug(f"'{password_set}' - default set for password generation.")
        password = ''.join(random.choices(password_set, k=length))
        return password

    # If a character set is provided, use it to generate the password
    if character_set:
        generated_set = set_generator(character_set)
        password = ''.join(random.choices(generated_set, k=length))

    # If a template is provided, use it to generate the password
    if template:
        password = check_template(template)

    return password


def main():
    """
    Main function to handle command-line arguments and generate passwords.
    """

    parser = argparse.ArgumentParser(
        description=r"""
        The password generator can create passwords using patterns.
        A pattern is a string defining the layout of the new password. 
        EXAMPLE:
        u{4}d{3}\-l{2} => DHRF345-st
        u{4}[dl]{3}-l{2} => DHRF3s4-st | FHGFds4-vt | DERS774-sd       
        """,
        epilog=r"""
        Placeholder         Type              Character Set
        d           Digit                      0123456789
        l           Lower-Case Letter          cabcdefghijklmnopqrstuvwxyz
        L           Mixed-Case Letter          ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz
        u           Upper-Case Letter          ABCDEFGHIJKLMNOPQRSTUVWXYZ
        p           Punctuation                ,.;:
        \           Escape (Fixed Char)        Use following character as is.
        {n}         Escape (Repeat)            Repeat the previous placeholder n times.
        [...]       Custom Char Set            Define a custom character set
        
        set option supported placeholders: Digit,Lower-Case Letter,
        Mixed-Case Letter, Upper-Case Letter, Punctuation, Escape (Fixed Char)
        """,
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument('-n', '--length', type=int, help='Set length of password')
    parser.add_argument('-f', '--file', help='Getting list of patterns from file'
                                             ' and generate for each random password')
    parser.add_argument('-t', '--template', help='Set template for generate passwords')
    parser.add_argument('-S', '--set', help='Character set')
    parser.add_argument('-c', '--count', type=int, default=1, help='Number of passwords')
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help='Verbose mode (-v |-vv |-vvv )')
    parser.add_argument('-l', '--log', help='Log file path')
    args = parser.parse_args()

    # Check for conflicting options
    if args.template and args.set:
        logging.error('Using -s and -t options. Please choose only one')
        exit(ERROR_BAD_OPTION)

    if args.set and args.file:
        logging.error('Using -s and -f options. Please choose only')
        exit(ERROR_BAD_OPTION)

    # Set up logging based on verbosity level
    if args.verbose or args.log:
        setup_logging(args.verbose, args.log)
        logging.debug('Using verbose mode')
        if args.log:
            logging.debug(f'Logging to file: {args.log}')

    # Generate passwords based template
    if args.template:
        for _ in range(args.count):
            if args.length:
                logging.error(f'Using -n option with -t')
                exit(ERROR_BAD_OPTION)
            logging.debug('Using template mod')
            password = generate_password(len(args.template), template=args.template)
            logging.info(f'Generated password length: {len(password)}')
            logging.info(f'Generated password from template: {"*" * len(password)}')
            print(password)

    # Generate password based on length
    if args.length:
        for _ in range(args.count):
            if args.set:
                logging.warning(f'Using -s with -n')
                continue
            try:
                password = generate_password(args.length)
                logging.info(f'Generated password: {"*" * len(password)}')
                logging.info(f'Generated password length: {len(password)}')
                print(password)
            except ValueError:
                logging.error(f'Invalid argument : {args.length}')
                exit(ERROR_BAD_OPTION)

    # Generate password based on set
    if args.set:
        for _ in range(args.count):
            logging.debug('Using set mode')
            password = generate_password(length=args.length, character_set=args.set)
            logging.info(f'Generated password length: {len(password)}')
            logging.info(f'Generated password are: {"*" * len(password)}')
            print(password)

    # Generate password using template from file
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as file:
                logging.info(f'Reading from file: {args.file}')
                templates = file.read()
                password = generate_password(length=len(templates), template=templates)
                logging.info(f'Generated password from file template: {"*" * len(password)}')
                logging.info(f'Generated password are: {"*" * len(password)}')
                print(password)
        except FileNotFoundError:
            logging.error(f'File {args.file} does not exist')
            exit(FILE_NOT_FOUND)
        except PermissionError:
            logging.error(f'Permission denied for file: {args.file}')
            exit(PERMISSION_DENIED)


if __name__ == '__main__':
    main()
