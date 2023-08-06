# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

import trytond.tests.test_tryton
import unittest

from trytond.modules.cashbook.tests.test_type import TypeTestCase
from trytond.modules.cashbook.tests.test_book import BookTestCase
from trytond.modules.cashbook.tests.test_line import LineTestCase
from trytond.modules.cashbook.tests.test_splitline import SplitLineTestCase
from trytond.modules.cashbook.tests.test_config import ConfigTestCase
from trytond.modules.cashbook.tests.test_category import CategoryTestCase
from trytond.modules.cashbook.tests.test_reconciliation import ReconTestCase
from trytond.modules.cashbook.tests.test_bookingwiz import BookingWizardTestCase
from trytond.modules.cashbook.tests.test_currency import CurrencyTestCase


__all__ = ['suite']


class CashbookTestCase(\
    CurrencyTestCase, \
    BookingWizardTestCase,\
    ReconTestCase,\
    CategoryTestCase,\
    ConfigTestCase,\
    LineTestCase,
    SplitLineTestCase,
    BookTestCase,
    TypeTestCase,
    ):
    'Test cashbook module'
    module = 'cashbook'

# end CashbookTestCase

def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(CashbookTestCase))
    return suite
