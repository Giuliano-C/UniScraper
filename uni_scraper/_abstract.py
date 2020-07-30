from bs4 import BeautifulSoup
from datetime import datetime
import json
import tabulate
from ._utils import on_exception_return, scrape_page

class AbstractScraper():

    def __getattribute__(self, name):
        to_return = None
        decorated_methods = [
            'courses',
            'course_detail',
            'units',
            'unit_detail'
        ]
        if name in decorated_methods:
            to_return = ''
        if name == 'courses':
            to_return = []
        if name == 'course_detail':
            to_return = 'No details found'
        if name == 'units':
            to_return = []
        if name == 'unit_detail':
            to_return = 'No details found'
        if to_return is not None:
            return on_exception_return(to_return)(object.__getattribute__(self, name))

        return object.__getattribute__(self, name)

    def courses(self):
        raise NotImplementedError("This should be implemented.")

    def units(self):
        raise NotImplementedError("This should be implemented.")

    def course_detail(self, **kwargs):
        raise NotImplementedError("This should be implemented.")

    def unit_detail(self, **kwargs):
        raise NotImplementedError("This should be implemented.")

    def save_json(self, out_file=None):
        current_date = int(datetime.now().timestamp() * 1000)
        if out_file is None:
            out_file = "{}_{}.json".format(self.abbreviation(), current_date)

        data = dict(
            name=self.name,
            abbreviation=self.abbreviation(),
            courses=self.courses(),
            units=self.units()
        )
        
        with open(out_file, 'w') as file:
            json.dump(data, file)

    def stdout(self):
        print("Name: {}".format(self.name))
        print("Abbreviation: {}".format(self.abbreviation()))

        print("Courses: ")
        courses = self.courses()
        header = courses[0]['programs'][0].keys()
        programs = []
        for course in courses:
            for program in course['programs']:
                programs.append(program)
        rows = [program.values() for program in programs]
        print(tabulate.tabulate(rows, header))

        print("Units: ")
        units = self.units()
        header = units[0].keys()
        rows = [unit.values() for unit in units]
        print(tabulate.tabulate(rows, header))