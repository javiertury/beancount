from beancount.core.amount import D
from beancount.core import data
from beancount.ops import auto_accounts
from beancount.parser import parsedoc
from beancount.parser import cmptest


class TestAutoInsertOpen(cmptest.TestCase):

    @parsedoc
    def test_auto_open(self, entries, _, options_map):
        """
        2014-02-01 *
          Assets:US:Bank:Checking     100 USD
          Assets:US:Bank:Savings     -100 USD

        2014-03-11 *
          Assets:US:Bank:Checking     100 USD
          Equity:Something
        """
        new_entries, _ = auto_accounts.auto_insert_open(entries, options_map)

        self.assertEqualEntries("""

        2014-02-01 open Assets:US:Bank:Savings
        2014-02-01 open Assets:US:Bank:Checking

        2014-02-01 *
          Assets:US:Bank:Checking     100 USD
          Assets:US:Bank:Savings     -100 USD

        2014-03-11 open Equity:Something

        2014-03-11 *
          Assets:US:Bank:Checking     100 USD
          Equity:Something

        """, new_entries)