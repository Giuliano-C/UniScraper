from tests import ScraperTest
from uni_scraper import UniversityOfSydney

class UniversityOfSydneyTest(ScraperTest):

    scraper_class = UniversityOfSydney

    def test_name(self):
        self.assertEqual("University of Sydney", self.harvester_class.name)

    def test_abbreviation(self):
        self.assertEqual("USYD", self.harvester_class.abbreviation())

    def test_courses(self):
        courses = self.harvester_class.courses()
        self.assertTrue(courses != [])
        self.assertTrue(type(courses) == list)

    def test_units(self):
        units = self.harvester_class.units()
        self.assertTrue(units != [])
        self.assertTrue(type(units) == list)

    def test_course_detail(self):
        course_detail = self.harvester_class.course_detail(degree_id=454)
        self.assertTrue(type(course_detail) == dict)
        self.assertEqual(course_detail['cp_required'], 192)
        self.assertEqual(course_detail['min_duration'], 4)
        self.assertEqual(len(course_detail['requirements']), 6)
        self.assertTrue(type(course_detail['planner']) == dict)

        course_detail = self.harvester_class.course_detail()
        self.assertEqual(course_detail, "No details found")

    def test_unit_detail(self):
        unit_detail = self.harvester_class.unit_detail(code='ENGG1111')
        self.assertTrue(type(unit_detail) == dict)
        self.assertEqual(unit_detail['code'], "ENGG1111")
        self.assertEqual(unit_detail['name'], "Integrated Engineering 1")

        unit_detail = self.harvester_class.unit_detail(code='AERO1400')
        self.assertTrue(type(unit_detail) == dict)
        self.assertEqual(unit_detail['code'], "AERO1400")
        self.assertEqual(unit_detail['name'], "Introduction to Aircraft Construction and Design")

        unit_detail = self.harvester_class.unit_detail()
        self.assertEqual(unit_detail, "No details found")

