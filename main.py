__author__ = 'vladimir'

import json

import yaml
import requests

from logger import Logger

log = Logger("rates")


class Adviser(object):
    CATEGORY = "DebitCardsOperations"
    ALL_CURRENCIES = ("RUR", "USD", "EUR")

    def __init__(self):
        self.url = "https://www.tinkoff.ru/api/v1/currency_rates/"
        with open("config.yaml", "r") as f:
            self.config = yaml.load(f)
        self.values = {}
        for item in self.ALL_CURRENCIES:
            self.values[item] = {
                "my_amount": self.config.get(item)
            }

    def __filter_data(self, data):
        """Removes extra data and filter all rates by currencies"""
        for item in data:
            if not (item["category"] != self.CATEGORY or item["fromCurrency"]["name"] not in self.ALL_CURRENCIES
                    or item["toCurrency"]["name"] not in self.ALL_CURRENCIES):
                name = item["fromCurrency"]["name"]
                if name not in self.values:
                    self.values[name] = {}
                self.values[name][item["toCurrency"]["name"]] = {
                    "sell": item["sell"],   # ! bank sells
                    "buy": item["buy"],     # ! bank buys
                }
        print json.dumps(self.values, indent=2)

    def __load_rates(self):
        """Initialize loading action"""
        try:
            data = requests.get(self.url).json()
            self.__filter_data(data["payload"]["rates"])
        except Exception as e:
            log.error("load_rates error: {}".format(repr(e)))

    def help(self):
        """Calculate all variants"""
        self.__load_rates()

        # case1: EUR[RUR]
        case1 = ""

        # case2: USD[RUR]

        # case3: EUR[USD]

        # case4: USD[EUR]

        # case5: (EUR[USD] + USD)[RUR]

        # case6: (USD[EUR] + EUR)[RUR]

        # and some extra cases:
        # case7: RUR[USD]

        # case8: RUR[USD] + EUR[USD]

        # case8: RUR[EUR] + USD[EUR]


if __name__ == "__main__":
    adviser = Adviser()
    adviser.help()
