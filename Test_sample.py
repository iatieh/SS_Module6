# tests/test_sample.py
import unittest
from utils import generate_checksum

class TestUtils(unittest.TestCase):
    def test_generate_checksum(self):
        content = b"test content"
        checksum = generate_checksum(content)
        self.assertEqual(checksum, "d8e8fca2dc0f896fd7cb4cb0031ba249")

if __name__ == '__main__':
    unittest.main()
