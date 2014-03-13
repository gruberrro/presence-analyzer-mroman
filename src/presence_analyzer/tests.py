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

    def test_mean_time_weekday_view(self):
        """
        Test mean time in weekday review
        """
        resp = self.client.get('/api/v1/mean_time_weekday/11')
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')

        expected_result = [
            [u'Mon', 24123.0],
            [u'Tue', 16564.0],
            [u'Wed', 25321.0],
            [u'Thu', 22984.0],
            [u'Fri', 6426.0],
            [u'Sat', 0],
            [u'Sun', 0]
        ]

        self.assertEqual(data, expected_result)

    def test_mean_t_week_view_emp_lst(self):
        """
        Test mean time in weekday review for empty list
        """
        resp = self.client.get('/api/v1/mean_time_weekday/199')
        data = json.loads(resp.data)
        empty_lst = []
        self.assertEqual(data, empty_lst)

    def test_presence_weekday_view(self):
        """
        Test presence time of given user grouped by weekday.
        """
        resp = self.client.get('/api/v1/presence_weekday/11')
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')

        exp_result = [
            [u'Weekday', u'Presence (s)'],
            [u'Mon', 24123],
            [u'Tue', 16564],
            [u'Wed', 25321],
            [u'Thu', 45968],
            [u'Fri', 6426],
            [u'Sat', 0],
            [u'Sun', 0],
        ]
        self.assertEqual(data, exp_result)

    def test_presence_week_view_emp_lst(self):
        """
        Test mean presence weekday review for empty list
        """
        resp = self.client.get('/api/v1/presence_weekday/199')
        data = json.loads(resp.data)
        empty_lst = []
        self.assertEqual(data, empty_lst)


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

    def test_group_by_weekly(self):
        """
        Test group_by_weekday function
        """
        empty_items = []
        items = {
            datetime.date(2013, 9, 11): {
                'end': datetime.time(16, 15, 27),
                'start': datetime.time(9, 13, 26)
            },
            datetime.date(2013, 9, 12): {
                'end': datetime.time(16, 41, 25),
                'start': datetime.time(10, 18, 36)
            }}
        result_1 = utils.group_by_weekday(items)
        result_2 = utils.group_by_weekday(empty_items)

        expected_result_1 = {
            0: [],
            1: [],
            2: [25321],
            3: [22969],
            4: [],
            5: [],
            6: [],
        }

        expected_result_2 = {
            0: [],
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
            6: [],
        }

        self.assertDictEqual(result_1, expected_result_1)
        self.assertDictEqual(result_2, expected_result_2)

    def test_seconds_since_midnight(self):
        """
        Test seconds_since_midnight function
        """
        input_time_format = datetime.datetime(2014, 3, 11, 14, 26, 25, 230847)
        result_time_for_input = utils.seconds_since_midnight(input_time_format)
        self.assertEqual(result_time_for_input, 51985)

    def test_interval(self):
        """
        Test interval function
        """
        t_start = datetime.datetime.now().time()
        t_end = datetime.datetime.now().time()
        input_time_1 = datetime.datetime(2014, 3, 11, 14, 26, 25, 230847)
        input_time_2 = datetime.datetime(2014, 3, 11, 14, 29, 25, 230847)
        result_time_for_input = utils.interval(input_time_1, input_time_2)

        self.assertLessEqual(t_start, t_end)
        self.assertEqual(result_time_for_input, 180)

    def test_mean(self):
        """
        Test mean function
        """
        strange_lst = [3, 4, 5, 6, 7, 8]
        empty_lst = []
        self.assertEqual(0, utils.mean(empty_lst))
        self.assertEqual(utils.mean(strange_lst), 5.5)


def suite():
    """
    Default test suite.
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PresenceAnalyzerViewsTestCase))
    suite.addTest(unittest.makeSuite(PresenceAnalyzerUtilsTestCase))
    return suite


if __name__ == '__main__':
    unittest.main()
