import unittest

from domain.data import Transaction
from decimal import Decimal


class TestData(unittest.TestCase):
    def test_transaction(self):
        with self.assertRaises(TypeError) as cm:
            Transaction('Mar 22',
                        2502.23,
                        Decimal('25'),
                        Decimal('25'),
                        Decimal('25'),
                        Decimal('25'),
                        Decimal('25'))
        self.assertEqual("Field 'start_balance' must be of type 'Decimal'.",
                         str(cm.exception))