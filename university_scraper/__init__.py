import os

from inspect import isclass
from importlib import import_module

# Suppress Driver Manager log
os.environ['WDM_LOG_LEVEL'] = '0'
os.environ['WDM_PRINT_FIRST_LINE'] = 'False'

UNIS = {}

module = import_module(".universities", package='university_scraper')
for attribute_name in dir(module):
    attribute = getattr(module, attribute_name)
    if isclass(attribute):
        UNIS[attribute.abbreviation()] = attribute


class UniversityNotImplementedError(NotImplementedError):
    '''Error when the university is not supported by this library'''
    pass


def available():
    return list(UNIS.keys())


def init(abbreviation):
    try:
        uni = UNIS[abbreviation]
    except KeyError:
        raise UniversityNotImplementedError(
            "University ({}) is not supported".format(abbreviation))
    return uni()


__all__ = ['available', 'init']
