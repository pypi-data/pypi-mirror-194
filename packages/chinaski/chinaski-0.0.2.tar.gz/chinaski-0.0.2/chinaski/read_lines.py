def read_lines_from_file(filename: str) -> list[str]:
    """Reads lines from a file and returns them as list of str.

    :param filename: file name to read lines from
    :return: list of str containing each line
    """
    with open(filename, "r") as file:
        return file.readlines()
