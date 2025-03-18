# tests/test_dialogflow.py
import unittest
from ai.dialogflow_handler import get_dialogflow_response

class TestDialogflow(unittest.TestCase):
    def test_get_dialogflow_response(self):
        response = get_dialogflow_response(12345, "Hello", "en")
        self.assertIsInstance(response, str)

if __name__ == '__main__':
    unittest.main()