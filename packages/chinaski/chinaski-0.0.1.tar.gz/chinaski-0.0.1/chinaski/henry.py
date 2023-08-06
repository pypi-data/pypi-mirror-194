import ntpath

import chinaski.read_lines as rl
from chinaski.finder import find_emails_in_line
from chinaski.is_email import Result, is_email


def path_leaf(path: str) -> str:
    """Retrieves the file name and extension from a given path.

    It should work in different OS.

    Obtained from:
    https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format

    :param path: path to retrieve the file from
    :return: str with the file name and extension
    """
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


class FilePathIsNotValidException(Exception):
    def __init__(self, message="The given file path is not valid"):
        super().__init__(message)


def core(file_path: str) -> list[Result]:
    """Core function of the program.

    It will read the lines from a given file and return a list of Result where it has found emails.

    :param file_path: path to file to detect emails in it
    :return: list of Result, containing the findings
    """
    if file_path == "" or file_path is None:
        raise FilePathIsNotValidException

    lines = rl.read_lines_from_file(filename=file_path)
    results = []
    file_name = path_leaf(file_path)

    for i in range(len(lines)):
        line = lines[i]
        emails_in_line = find_emails_in_line(line)

        for email in emails_in_line:
            res = is_email(line=email, line_number=i + 1, file_name=file_name)
            if res:
                results.append(res)

    return results
