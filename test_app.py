import unittest
from app import app
import json

class TestFinanceApp(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_homepage_loads(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_api_returns_all_assets(self):
        response = self.app.get('/api/data')
        data = json.loads(response.data)
        
        # Verify all 5 assets exist
        self.assertTrue('aapl' in data)
        self.assertTrue('tsla' in data)
        self.assertTrue('googl' in data)
        self.assertTrue('btc' in data)
        self.assertTrue('eth' in data)
        
        # Check integrity of one asset
        self.assertGreater(data['tsla']['price'], 0)

if __name__ == '__main__':
    unittest.main()