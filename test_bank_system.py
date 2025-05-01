# File: test_bank_system.py

import unittest
from unittest.mock import MagicMock, patch
import main

class TestBankSystem(unittest.TestCase):
#I am not sure what I am doing so this may not work
    def setUp(self):
        self.connection = MagicMock()
        self.cursor = MagicMock()
        self.connection.cursor.return_value = self.cursor
        main.connection = self.connection

    def test_login_success(self):
        self.cursor.fetchone.return_value = (1, 'Alice', 1234567890, 'pass', 100.0)
        user = main.login(self.cursor)
        self.assertIsNotNone(user)

    def test_login_fail(self):
        self.cursor.fetchone.return_value = None
        with patch('builtins.input', side_effect=['Alice', '1234567890', 'wrongpass', 'no']):
            user = main.login(self.cursor)
            self.assertIsNone(user)

    def test_create_account(self):
        self.cursor.fetchone.return_value = (1, 'Bob', 9876543210, 'pass', 0.0)
        with patch('builtins.input', side_effect=['Bob', 'pass']):
            user = main.create_account(self.cursor)
            self.assertEqual(user[1], 'Bob')

    def test_deposit_money(self):
        with patch('builtins.input', return_value='50'):
            main.deposit_money(self.cursor, self.connection, (1, 'Test'))
            self.cursor.execute.assert_called()
            self.connection.commit.assert_called()

    def test_withdraw_money(self):
        self.cursor.fetchone.return_value = [100.0]
        with patch('builtins.input', return_value='30'):
            main.withdraw_money(self.cursor, self.connection, (1, 'Test'))
            self.cursor.execute.assert_called()
            self.connection.commit.assert_called()

    def test_close_account(self):
        with patch('builtins.input', return_value='yes'):
            result = main.close_account(self.cursor, self.connection, (1, 'Test'))
            self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
