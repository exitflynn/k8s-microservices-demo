import unittest
from flask import Flask
from cdn_server import app

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), "Hey there! To send a file, use the /upload endpoint.")

    def test_upload_file_no_file(self):
        response = self.app.post('/upload')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'No file provided', response.data)

    def test_upload_file_no_selected_file(self):
        data = {'file': ''}
        response = self.app.post('/upload', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'No file provided', response.data)


if __name__ == '__main__':
    unittest.main()
