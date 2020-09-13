import re


def get_int_from_string(string):
    return int(re.search(r'\d+', string).group())
