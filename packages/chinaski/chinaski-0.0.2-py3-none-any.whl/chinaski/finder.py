import re


def find_emails_in_line(line: str) -> list[str]:
    """Finds emails given a str and returns them as items of a list.

    Obtained from:
    https://stackoverflow.com/questions/17681670/extract-email-sub-strings-from-large-document

    :param line: str to find emails in
    :return: list of emails found or empty list is nothing is found
    """
    return re.findall(r"[\w.+-]+@[\w-]+\.[\w.-]+", line)
