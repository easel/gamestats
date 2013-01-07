from django.contrib.auth.models import User
from django.test import TestCase
from os.path import dirname, join
from gamestats.loot.fixtures import initial_data
from gamestats.loot.submission import parse_xml

class SubmissionTestCase(TestCase):
    """
    Test submission workflows
    """

    def setUp(self):
        """
        Set up the Case
        """
        initial_data.apply()
        self.data_path = join(dirname(__file__), 'data', 'test.xml')

    def test_submit_xml(self):
        """
        Test parsing an XML submission
        """
        xml = file(self.data_path).read()
        parse_xml(xml)


