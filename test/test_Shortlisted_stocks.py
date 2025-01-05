import unittest
from lambda_function import lambda_handler
import json

class TestShortlistedStocks(unittest.TestCase):

    def setUp(self):
        self.context = {}
        self.post_event = {
            "body": json.dumps({
                "ID": "12345",
                "Date": "2023-10-01",
                "StockName": "ABC Corp",
                "Price": 150.75,
                "Volume": 1000
            })
        }
        self.put_event = {
            "body": json.dumps({
                "ID": "12345",
                "Date": "2023-10-01",
                "StockName": "XYZ Corp",
                "Price": 200.50,
                "Volume": 1500
            })
        }
        self.delete_event = {
            "body": json.dumps({
                "ID": "12345",
                "Date": "2023-10-01"
            })
        }

    def test_post_item(self):
        response = lambda_handler(self.post_event, self.context)
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('Item updated successfully', response['body'])

    def test_put_item(self):
        response = lambda_handler(self.put_event, self.context)
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('Item updated successfully', response['body'])

    def test_delete_item(self):
        response = lambda_handler(self.delete_event, self.context)
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('Item updated successfully', response['body'])

if __name__ == '__main__':
    unittest.main()
