import cStringIO
from elementtree.SimpleXMLWriter import XMLWriter
from os.path import dirname, join
from unittest import TestCase
from gamestats.eqlog.parser import Parser

class ParserTestCase(TestCase):
    """
    Test parser
    """

    def setUp(self):
        """
        standardize parser setup routines
        """
        self.data_path = join(dirname(__file__), 'data')
        self.log_path = join(self.data_path, 'testlog.txt')
        self.parser = Parser(extract=None, debug=True, myname = 'Bardeil')

    def test_logfile_parse(self):
        """
        test the basic parse method
        """
        #assert(False)
        self.parser.parse(self.log_path)
        outfile = file(join(self.data_path, 'test.xml'), 'w')
        outfile.write(self.parser.asXml())
