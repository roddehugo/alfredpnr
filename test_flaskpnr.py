# -*- coding: utf-8 -*-
import os
import flaskpnr
import unittest
import tempfile

###################
# Alfred PNR Unit Test #
###################


class FlaskPNRTestCase(unittest.TestCase):

    def setUp(self):
        flaskpnr.app.config['TESTING'] = True
        self.app = flaskpnr.app.test_client()

    def test_find_error(self):
        """
        Test with a totally random data
        Should throw an error
        """
        with self.assertRaisesRegexp(Exception, "We are unable to find this confirmation number"):
            self.app.get('/find/abcdef/smith')

    def test_find_ok(self):
        """
        Test with some special data
        """
        rv = self.app.get('/find/<pnr>/<name>')
        self.assertIn('yourname', rv.data)

if __name__ == '__main__':
    unittest.main()
