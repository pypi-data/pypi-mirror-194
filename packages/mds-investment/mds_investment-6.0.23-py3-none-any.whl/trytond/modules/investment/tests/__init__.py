# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

import trytond.tests.test_tryton
import unittest

from trytond.modules.investment.tests.test_asset import AssetTestCase
from trytond.modules.investment.tests.test_rate import RateTestCase
from trytond.modules.investment.tests.test_source import SourceTestCase
from trytond.modules.investment.tests.test_wizard import WizardTestCase


__all__ = ['suite']


class InvestmentTestCase(\
    WizardTestCase, \
    SourceTestCase, \
    RateTestCase,\
    AssetTestCase,\
    ):
    'Test investment module'
    module = 'investment'

# end InvestmentTestCase

def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(InvestmentTestCase))
    return suite
