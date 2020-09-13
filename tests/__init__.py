import unittest
import os

# Suppress Driver Manager log
os.environ['TESTING'] = 'true'
os.environ['WDM_LOG_LEVEL'] = '0'
os.environ['WDM_PRINT_FIRST_LINE'] = 'false'


class ScraperTest(unittest.TestCase):
    def setUp(self):
        self.harvester_class = self.scraper_class()
