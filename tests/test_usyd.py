from tests import ScraperTest
from ._utils import ignore_warnings
from university_scraper.universities import UniversityOfSydney


class UniversityOfSydneyTest(ScraperTest):

    scraper_class = UniversityOfSydney

    def test_name(self):
        self.assertEqual("University of Sydney", self.harvester_class.name)

    def test_abbreviation(self):
        self.assertEqual("USYD", self.harvester_class.abbreviation())

    @ignore_warnings
    def test_programs(self):
        programs = self.harvester_class.programs

        self.assertTrue(programs != [])
        self.assertTrue(type(programs) == list)
        program = programs[0]
        self.assertTrue(type(program['department']) == str)
        self.assertTrue(type(program['name']) == str)

    @ignore_warnings
    def test_units(self):
        units = self.harvester_class.units

        self.assertTrue(units != [])
        self.assertTrue(type(units) == list)
        unit = units[0]
        self.assertTrue(type(unit['code']) == str)
        self.assertTrue(type(unit['name']) == str)

    @ignore_warnings
    def test_program_detail(self):
        program_detail = self.harvester_class.program_detail(url='https://cusp.sydney.edu.au/students/view-degree-page/degree_id/454')

        self.assertTrue(type(program_detail) == dict)
        self.assertEqual(type(program_detail['schedule']), list)
        self.assertEqual(type(program_detail['groups']), list)
        self.assertEqual(program_detail['cp_required'], 192)
        self.assertEqual(program_detail['min_duration'], 4)
        self.assertEqual(program_detail['min_duration'], 4)

        program_detail = self.harvester_class.program_detail(url='')
        self.assertEqual(program_detail, {})

    @ignore_warnings
    def test_unit_detail(self):
        unit_detail = self.harvester_class.unit_detail('ENGG1111')

        self.assertTrue(type(unit_detail) == dict)
        self.assertEqual(unit_detail['code'], "ENGG1111")
        self.assertEqual(type(unit_detail['code']), str)
        self.assertEqual(unit_detail['name'], "Integrated Engineering 1")
        self.assertEqual(type(unit_detail['name']), str)
        self.assertEqual(unit_detail['credit_points'], 6)
        self.assertEqual(type(unit_detail['credit_points']), int)
        self.assertEqual(type(unit_detail['sessions']), list)
        self.assertEqual(type(unit_detail['assessments']), list)

        unit_detail = self.harvester_class.unit_detail('')
        self.assertEqual(unit_detail, {})
