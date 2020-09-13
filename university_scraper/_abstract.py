

class AbstractScraper():

    def __init__(self):
        self._programs = None
        self._units = None

    @staticmethod
    def abbreviation():
        raise NotImplementedError("This needs to be implemented.")

    @property
    def programs(self):
        raise NotImplementedError("This needs to be implemented.")

    @property
    def units(self):
        raise NotImplementedError("This needs to be implemented.")

    def program_detail(self, identifier):
        raise NotImplementedError("This should be implemented.")

    def unit_detail(self, identifier):
        raise NotImplementedError("This should be implemented.")
