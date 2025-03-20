import unittest
from bot.app import app

class TestHelloWorld(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
    def test_hello_world(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Hello, World!')

    def test_msg(self):
        response = self.app.post('/msg', json={'msg': 'test'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {'msg': 'test'})
        
if __name__ == '__main__':
    unittest.main() 