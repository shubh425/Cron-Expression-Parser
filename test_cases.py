import unittest
import re
from CronExpressionParser import *

class TestParse(unittest.TestCase):
    def test_empty_input(self):
        self.assertRaises(TypeError, parse, "")

    def test_invalid_type_input(self):
        self.assertRaises(TypeError, parse, [])

    def test_invalid_format(self):
        self.assertRaises(TypeError, parse, "1 2 3 4 5")
        self.assertRaises(ValueError, parse, "a * 1 2 4 /usr/bin/foo")

    def test_invalid_range(self):
        self.assertRaises(IndexError, parse, "60 * * * * /usr/bin/foo")

    def test_minute_parser(self):
        self.assertEqual(number_parser("minute", "0"), "0")
        self.assertEqual(number_parser("minute", "59"), "59")
        self.assertRaises(IndexError, number_parser, "minute", "60")

    def test_hour_parser(self):
        self.assertEqual(number_parser("hour", "0"), "0")
        self.assertEqual(number_parser("hour", "23"), "23")
        self.assertRaises(IndexError, number_parser, "hour", "24")

    def test_day_of_month_parser(self):
        self.assertEqual(number_parser("dayOfMonth", "1"), "1")
        self.assertEqual(number_parser("dayOfMonth", "31"), "31")
        self.assertRaises(IndexError, number_parser, "dayOfMonth", "32")

    def test_month_parser(self):
        self.assertEqual(number_parser("month", "1"), "1")
        self.assertEqual(number_parser("month", "12"), "12")
        self.assertRaises(IndexError, number_parser, "month", "13")

    def test_day_of_week_parser(self):
        self.assertEqual(number_parser("dayOfWeek", "1"), "1")
        self.assertEqual(number_parser("dayOfWeek", "7"), "7")
        self.assertRaises(IndexError, number_parser, "dayOfWeek", "8")

    def test_comma_parser(self):
        self.assertEqual(comma_parser("minute", "1,2,3"), "1 2 3")
        self.assertEqual(comma_parser("hour", "0,12,23"), "0 12 23")
        self.assertRaises(IndexError,comma_parser, "minute", "60,3,1")
        self.assertRaises(IndexError,comma_parser, "dayOfWeek", "0,1,5")

    def test_range_parser(self):
        self.assertEqual(range_parser("minute", "0-30"), "0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30")
        self.assertEqual(range_parser("hour", "9-17"), "9 10 11 12 13 14 15 16 17")
        self.assertRaises(IndexError, range_parser, "dayOfMonth", "1-32")
        self.assertRaises(IndexError, range_parser, "dayOfMonth", "10-5")

    def test_star_parser(self):
        self.assertEqual(star_parser("minute", "*"), "0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59")
        self.assertEqual(star_parser("hour", "*"), "0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23")

    def test_step_parser(self):
        self.assertEqual(step_parser("minute", "*/5"), "0 5 10 15 20 25 30 35 40 45 50 55")
        self.assertEqual(step_parser("minute", "5/10"), "5 15 25 35 45 55")
        self.assertRaises(IndexError, step_parser, "minute", "60/5")
        self.assertRaises(IndexError, step_parser, "dayOfWeek", "0/2")
    
if __name__ == '__main__':
    unittest.main()

