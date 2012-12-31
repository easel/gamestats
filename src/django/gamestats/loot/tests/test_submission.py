from django.test import TestCase
from os.path import dirname, join

class SubmissionTestCase(TestCase):
    """
    Test submission workflows
    """

    def setUp(self):
        """
        Set up the Case
        """
        self.data_path = join(dirname(__name__), 'test.xml')

    def test_submit_xml(self):
        """
        Test parsing an XML submission
        """
        xml = file(self.data_path).read()
        parse_xml(xml)


