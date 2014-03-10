# -*- coding: utf-8 -*-
"""
Presence analyzer unit tests.
"""
import os.path
import json
import datetime
import unittest

from presence_analyzer import main, views, utils


TEST_DATA_CSV = os.path.join(
    os.path.dirname(__file__), '..', '..', 'runtime', 'data', 'test_data.csv'
)
<<<<<<< HEAD

=======
TEST_DATA_BAD_CSV = os.path.join(
    os.path.dirname(__file__), '..', '..', 'runtime', 'data', 'test_data_bad.csv' 
)
>>>>>>> 4f752dd... [#1411] New 4 tests added

# pylint: disable=E1103
class PresenceAnalyzerViewsTestCase(unittest.TestCase):
    """
    Views tests.
    """

    def setUp(self):
        """
        Before each test, set up a environment.
        """
        main.app.config.update({'DATA_CSV': TEST_DATA_CSV})
        self.client = main.app.test_client()

    def tearDown(self):
        """
        Get rid of unused objects after each test.
        """
        pass

    def test_mainpage(self):
        """
        Test main page redirect.
        """
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 302)
        assert resp.headers['Location'].endswith('/presence_weekday.html')

    def test_api_users(self):
        """
        Test users listing.
        """
        resp = self.client.get('/api/v1/users')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)
        self.assertDictEqual(data[0], {u'user_id': 10, u'name': u'User 10'})


class PresenceAnalyzerUtilsTestCase(unittest.TestCase):
    """
    Utility functions tests.
    """

    def setUp(self):
        """
        Before each test, set up a environment.
        """
        main.app.config.update({'DATA_CSV': TEST_DATA_CSV})

    def tearDown(self):
        """
        Get rid of unused objects after each test.
        """
        pass

    def test_get_data(self):
        """
        Test parsing of CSV file.
        """
        data = utils.get_data()
        self.assertIsInstance(data, dict)
        self.assertItemsEqual(data.keys(), [10, 11])
        sample_date = datetime.date(2013, 9, 10)
        self.assertIn(sample_date, data[10])
        self.assertItemsEqual(data[10][sample_date].keys(), ['start', 'end'])
        self.assertEqual(data[10][sample_date]['start'],
                         datetime.time(9, 39, 5))
<<<<<<< HEAD


def suite():
=======
        #with self.assertRaises(ValueError):  #tu zmienione - pozniej usun
        #    utils.get_data()                 #tu zmienione - pozniej usun
        #main.app.config.update({'DATA_CSV': TEST_DATA_BAD_CSV})  # tu bylo ok
        #utils.get_data()                                         # tu bylo ok 
    def test_group_by_weekly(self):
        items = []
        result = utils.group_by_weekday(items)
        expected_result = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
        self.assertDictEqual(result, expected_result)

    def test_seconds_since_midnight(self):
        time = datetime.datetime.now().time()
        expected_time_format = 253
        result_time = utils.seconds_since_midnight(time)
        self.assertEqual(type(expected_time_format), type(result_time))

    def test_interval(self):
        int_data = 233
        t_start = datetime.datetime.now().time()
        t_end = datetime.datetime.now().time()
        inter_of_time = utils.interval(t_start, t_end)

        self.assertEqual(type(int_data), type(inter_of_time))
        self.assertLessEqual(t_start, t_end)

    def test_mean(self):
        float_data = 0.5245
        strange_lst = [3,4,5,6,7,8]
        empty_lst = []
        self.assertEqual(0, utils.mean(empty_lst))
        self.assertEqual(type(float_data), type(utils.mean(strange_lst)))

    def suite():
>>>>>>> 4f752dd... [#1411] New 4 tests added
    """
    Default test suite.
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PresenceAnalyzerViewsTestCase))
    suite.addTest(unittest.makeSuite(PresenceAnalyzerUtilsTestCase))
    return suite


if __name__ == '__main__':
    unittest.main()
