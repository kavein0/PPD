import logging
import os


def setup_logging(verbosity: int, log_file: str = None) -> None:
    """
    Set up logging based on the verbosity level and optional log file.

    :param verbosity: Verbosity level (1(WARNING), 2(INFO), 3(DEBUG)).
    :param log_file: Optional file to log to.
    """
    level = {
        1: logging.WARNING,
        2: logging.INFO,
        3: logging.DEBUG
    }.get(verbosity, logging.WARNING)

    if log_file:
        log_file_path = os.path.join('loggin', log_file)
        logging.basicConfig(filename=log_file_path, level=level, format='%(asctime)s\t%(levelname)s\t%(message)s')
    else:
        logging.basicConfig(level=level, format='%(levelname)s\t %(message)s')
