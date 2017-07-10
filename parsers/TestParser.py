import unittest
import Parser.py
import json

class TestParser(unittest.TestCase):

    def test_extractInfoFromFile(self):
        self.assertEqual(, )

if __name__ == '__main__':
    unittest.main()

fileName = "baikeData/dataBaike.json"
parsed = json.loads(fileName, encoding='utf-8')
print(json.dumps(parsed, indent=4,sort_keys=True))

