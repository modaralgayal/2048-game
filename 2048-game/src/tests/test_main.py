import unittest
from src.main import main


class TestMainFunction(unittest.TestCase):
    "Tests for main function"

    def test_main_function(self):
        result = main()
        assert result == "Hello World"



