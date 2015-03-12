import unittest
from app.app import get_html


class TestGetHtml(unittest.TestCase):

    def test_get_html(self):
        test_text = "<!-- SHTML Wrapper - 500 Server Error -->\n[an error occurred while processing this directive]\n"
        self.assertEqual(get_html('pauliukonis.com/500.shtml'), test_text)

    def test_get_html_with_protocol(self):
        test_text = "<!-- SHTML Wrapper - 500 Server Error -->\n[an error occurred while processing this directive]\n"
        self.assertEqual(get_html('http://pauliukonis.com/500.shtml'), test_text)

    def test_invalid_file(self):
        self.assertEqual(get_html('gobbledygook'), None)