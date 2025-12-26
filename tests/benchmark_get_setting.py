import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import get_setting, update_settings, app

class TestGetSettingPerformance(unittest.TestCase):
    def setUp(self):
        # Clear lru_cache if it exists
        if hasattr(get_setting, 'cache_clear'):
            get_setting.cache_clear()

    @patch('app.get_db_connection')
    def test_get_setting_db_calls(self, mock_get_db):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {'setting_value': 'test_value'}

        # First call
        val1 = get_setting('test_key')
        self.assertEqual(val1, 'test_value')

        # Second call
        val2 = get_setting('test_key')
        self.assertEqual(val2, 'test_value')

        # Third call
        val3 = get_setting('test_key')
        self.assertEqual(val3, 'test_value')

        # With caching, DB connection should be created only ONCE
        self.assertEqual(mock_get_db.call_count, 1, f"Expected 1 DB connection, but got {mock_get_db.call_count}")

if __name__ == '__main__':
    unittest.main()
