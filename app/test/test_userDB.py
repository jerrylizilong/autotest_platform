from app import useDB
import unittest,time

class TestUseDB(unittest.TestCase):
    def test_search(self):
        result = useDB.useDB().search('select value from test_config where name = "defaultBrowser";')
        self.assertEqual(len(result),1)
        self.assertEqual(result[0][0],'Chrome')

    def test_insert(self):
        newValue = str(time.time())
        useDB.useDB().insert('update test_config set value = "%s" where  name = "unittest";' %newValue)
        time.sleep(2)
        result = useDB.useDB().search('select value from test_config where name = "unittest";')[0][0]
        self.assertEqual(result,newValue)


if __name__ == '__main__':
    unittest.main()