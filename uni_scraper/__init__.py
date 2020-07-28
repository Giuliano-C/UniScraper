import re
from .usyd import UniversityOfSydney

UNIS = {
    UniversityOfSydney.abbreviation(): UniversityOfSydney,
}

class UniversityNotImplementedError(NotImplementedError):
    '''Error when the university is not supported by this library'''
    pass

def available():
    return list(UNIS.keys())

def load(abbreviation):
    try:
        uni = UNIS[abbreviation]
    except KeyError:
        raise UniversityNotImplementedError(
            "University ({}) is not supported".format(abbreviation))
    return uni()
    

__all__ = ['available', 'load']
name = "uni_scraper"