import json
import requests
import unittest
import logging
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
import rhclient.client as client

host = os.environ.get('RH_HOST', 'localhost')
port = os.environ.get('RH_PORT', '5000')
client.configUrl(f"http://{host}:{port}")

class test_py_client(unittest.TestCase) :
    @classmethod
    def setUpClass(self) -> None:
            print('\n\n###################################    Testing Overall Python Client    #############################################\n\n')
            logging.info(f"Testing {__class__.__name__}")
            return super().setUpClass()

    @classmethod
    def tearDownClass(self) -> None:
            client = None
            print('\n\n###################################    Done Testing Overall Python Client    #############################################\n\n')
            return super().tearDownClass()

    def test_01_create(self):
        client.create_path('/test', 200, 'test <strong>test</strong> test', headers={"Content-Type": "text/html"})
        actual = client.get_path('/test')
        self.assertEqual(0, actual["delay"])
        self.assertEqual("/test", actual["name"])
        self.assertEqual({"Content-Type": "text/html"}, actual["headers"])
        self.assertEqual(200, actual["return_code"])
        self.assertEqual("test <strong>test</strong> test", actual["return_value"])
        client.delete_path('/test')

    def test_02_create_another(self) :
        client.create_path('/test', 202, 'test <em>test2</em> test')
        actual = client.get_path('/test')
        self.assertEqual(0, actual["delay"])
        self.assertEqual("/test", actual["name"])
        self.assertEqual({"Content-Type": "application/json"}, actual["headers"])
        self.assertEqual(202, actual["return_code"])
        self.assertEqual("test <em>test2</em> test", actual["return_value"])
        client.delete_path('/test')

    # def test_03_creation_fail(self) :
    #     client.create_path('/test2', 202, 'test2 <em>test2</em> test2')
    #     cl2 = PyRH_Client(f"http://{host}:{port}/test2")
    #     print("\nEndpoint creation failure:")
    #     expected = f"\nPath creation Failed!\nStatus_code: 202,\nUrl: http://{host}:{port}/test2,\nError_text: ACCEPTED"
    #     actual = cl2.create_path('/breakMe', 500, 'I WILL BREAK ON PURPOSE TO DEMO THE ERROR HANDLER')
    #     self.assertEqual(expected, actual)
    #     cl2 = None
    #     client.delete_path('/test2')

    def test_04_read(self):
        client.create_path('/test', 200, 'test <strong>test</strong> test')
        actual = client.get_path('/test')
        self.assertEqual(0, actual["delay"])
        self.assertEqual("/test", actual["name"])
        self.assertEqual({"Content-Type": "application/json"}, actual["headers"])
        self.assertEqual(200, actual["return_code"])
        self.assertEqual("test <strong>test</strong> test", actual["return_value"])
        client.delete_path('/test')

    def test_05_read_all(self):
        client.create_path('/test', 200, 'test <strong>test</strong> test')
        client.create_path('/test2', 202, 'test2 <em>test2</em> test2')
        print("\nRead_all path results:")
        # expected = "{'/test': {'delay': 0, 'headers': {'Content-Type': 'application/json'}, 'rc': 200, 'return_value': 'test <strong>test</strong> test'}, '/test2': {'delay': 0, 'headers': {'Content-Type': 'application/json'}, 'rc': 202, 'return_value': 'test2 <em>test2</em> test2'}}"
        actual = client.get_all()
        actual_1 = json.loads(actual[0])
        actual_2 = json.loads(actual[1])
        # print(expected)
        print(actual)
        # self.assertEqual(expected, actual)
        self.assertEqual(0, actual_1["delay"])
        self.assertEqual("/test", actual_1["name"])
        self.assertEqual({"Content-Type": "application/json"}, actual_1["headers"])
        self.assertEqual(200, actual_1["return_code"])
        self.assertEqual("test <strong>test</strong> test", actual_1["return_value"])
        self.assertEqual(0, actual_2["delay"])
        self.assertEqual("/test2", actual_2["name"])
        self.assertEqual({"Content-Type": "application/json"}, actual_2["headers"])
        self.assertEqual(202, actual_2["return_code"])
        self.assertEqual("test2 <em>test2</em> test2", actual_2["return_value"])
        client.delete_path('/test')
        client.delete_path('/test2')

    def test_06_update(self):
        client.create_path('/test', 200, 'test <strong>test</strong> test')
        print("\nUpdate path results:")
        client.update_path('/test', 300, 'I\'M AN UPDATE, LOOK AT ME ALL UPDATED!!!')
        actual = client.get_path('/test')
        self.assertEqual(0, actual["delay"])
        self.assertEqual("/test", actual["name"])
        self.assertEqual({"Content-Type": "application/json"}, actual["headers"])
        self.assertEqual(300, actual["return_code"])
        self.assertEqual('I\'M AN UPDATE, LOOK AT ME ALL UPDATED!!!', actual["return_value"])
        client.delete_path('/test')

    def test_07_delete(self):
        try :
            client.create_path('/test', 200, 'test <strong>test</strong> test')
            client.create_path('/test2', 202, 'test2 <em>test2</em> test2')
            client.delete_path('/test')
            client.delete_path('/test2')
        except :
            self.fail()

    def test_08_delete_multiple(self):
            client.create_path('/path1', 200, 'path test 1')
            client.create_path('/path2', 200, 'path test 2')
            client.create_path('/path3', 200, 'path test 3')
            try :
                client.delete_paths(['/path1', '/path2', '/path3'])
            except :
                self.fail()

    def test_09_delete_multiple_fail(self):
        self.skipTest("Not implemented on server")
        try:
            s, f = json.loads(client.delete_paths(['/path1', '/path2', '/path3']).decode('utf-8'))
            # print(s)
            self.assertEquals(s, {})
            self.assertEquals(f, {'/path1': 'Path /path1 does not exist in the currently stored paths.',
                                '/path2': 'Path /path2 does not exist in the currently stored paths.',
                                '/path3': 'Path /path3 does not exist in the currently stored paths.'})
        except:
            self.fail()

    # def test_10_create_path_with_other_host(self):
    #     client.configUrl("http://127.0.0.1:5000")
    #     client.create_path('/test', 200, 'test <strong>test</strong> test')
    #     expected = "New path created:\n/test:{'delay': 0, 'headers': {'Content-Type': 'application/json'}, 'rc': 200, 'return_value': 'test <strong>test</strong> test'}"
    #     actual = 'New path created:\n/test:{}'.format(client.get_path('/test'))
    #     self.assertEqual(expected, actual)
    #     # client.delete_path('/test')

if __name__ == "__main__" :
    unittest.main()
