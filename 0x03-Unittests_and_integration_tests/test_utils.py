#!/usr/bin/env python3
"""
Unittest for utils.access_nested_map
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)
#!/usr/bin/env python3
"""
Unittest for utils.access_nested_map
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), 'a'),
        ({"a": 1}, ("a", "b"), 'b'),
    ])
    def test_access_nested_map_exception(self, nested_map, path, missing_key):
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), f"'{missing_key}'")
from utils import get_json
from unittest.mock import patch, Mock
import unittest
from parameterized import parameterized


class TestGetJson(unittest.TestCase):
    """Tests for utils.get_json"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        mock_response = Mock()
        mock_response.json.return_value = test_payload

        with patch("utils.requests.get", return_value=mock_response) as mock_get:
            result = get_json(test_url)

            # Assert get_json returns expected payload
            self.assertEqual(result, test_payload)

            # Assert requests.get was called once with correct URL
            mock_get.assert_called_once_with(test_url)
# utils.py
import requests

def get_json(url):
    return requests.get(url).json()
from utils import memoize
from unittest.mock import patch
import unittest


class TestMemoize(unittest.TestCase):
    """Tests for utils.memoize decorator"""

    def test_memoize(self):
        """Test that a memoized method calls its original function only once"""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            obj = TestClass()
            result1 = obj.a_property()
            result2 = obj.a_property()

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()
def memoize(method):
    """Memoize decorator"""
    attr_name = "_{}".format(method.__name__)

    @property
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)

    return wrapper
from utils import memoize
from unittest.mock import patch
import unittest


class TestMemoize(unittest.TestCase):
    """Tests for utils.memoize decorator"""

    def test_memoize(self):
        """Test that a memoized method calls its original function only once"""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            obj = TestClass()
            result1 = obj.a_property()
            result2 = obj.a_property()

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()
def memoize(method):
    """Memoize decorator"""
    attr_name = "_{}".format(method.__name__)

    @property
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)

    return wrapper
#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from utils import memoize


class TestMemoize(unittest.TestCase):
    def test_memoize(self):
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            test_instance = TestClass()
            result1 = test_instance.a_property
            result2 = test_instance.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()
