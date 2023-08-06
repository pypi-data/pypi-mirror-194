# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

import trytond.tests.test_tryton
import unittest

from trytond.modules.cashbook_investment.tests.test_book import CbInvTestCase
from trytond.modules.cashbook_investment.tests.test_reconciliation import ReconTestCase
from trytond.modules.cashbook_investment.tests.test_yield import YieldTestCase


__all__ = ['suite']


class CashbookInvestmentTestCase(\
    CbInvTestCase,\
    ReconTestCase,\
    YieldTestCase,\
    ):
    'Test cashbook-investment module'
    module = 'cashbook_investment'

# end CashbookInvestmentTestCase

def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(CashbookInvestmentTestCase))
    return suite
