#!/usr/bin/env python3
""" Parameterize a unit test"""
import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """ Class for testing acces_nested_map """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """ Test access_nested_map with diff inputs """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """ Test access_nested_map to raise a KeyErr for invalid inputs """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)

        self.assertEqual(str(context.exception), "'{}'".format(path[-1]))


class TestGetJson(unittest.TestCase):
    """ Test class for the get_json fn """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        """ Test get_json with mocked requests.get """
        mock_resp = Mock()
        mock_resp.json.return_value = test_payload
        mock_get.return_value = mock_resp

        res = get_json(test_url)
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(res, test_payload)


class TestMemoize(unittest.TestCase):
    """ Class for the memoize deco """
    def test_memoize(self):
        """ Test that memoize caches the result of a_prop """
        class TestClass:
            def a_method(self):
                return 45

            @memoize
            def a_property(self):
                return self.a_method()

        tst = TestClass()

        with patch.object(tst, 'a_method', return_value=42) as mock:
            res1 = tst.a_property()
            rest2 = tst.a_property()
            mock.assert_called_once()
            self.assertEqual(res1, res2)
            self.assertEqual(res1, 42)
            


if __name__ == "__main__":
    unittest.main()