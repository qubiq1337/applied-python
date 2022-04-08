from unittest import TestCase

from homeworks.log_parse.log_parse import is_request

class Test(TestCase):
    def test_is_request(self):
        str = '[21/Mar/2018 21:32:09] "GET https://sys.mail.ru/static/css/reset.css HTTPS/1.1" 200 1090'
        self.assertEqual(True, is_request(str))

