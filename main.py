__author__ = 'vladimir'

import json

import yaml
import requests

from logger import Logger

log = Logger("rates")


class Adviser(object):
    CATEGORY = "DebitCardsOperations"
    ALL_CURRENCIES = ("RUB", "USD", "EUR")

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
        log.debug(json.dumps(self.values, indent=2))

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

        rub_amount = self.values["RUB"]["my_amount"]
        usd_amount = self.values["USD"]["my_amount"]
        eur_amount = self.values["EUR"]["my_amount"]
        all_cases = (
            {
                "name": "EUR[RUB]",
                "description": "Convert EUR to RUB",
                "dimension": "RUB",
                "value": eur_amount*self.values["EUR"]["RUB"]["buy"],
            },
            {
                "name": "USD[RUB]",
                "description": "Convert USD to RUB",
                "dimension": "RUB",
                "value": usd_amount*self.values["USD"]["RUB"]["buy"],
            },
            {
                "name": "EUR[USD]",
                "description": "Convert EUR to USD",
                "dimension": "USD",
                "value": eur_amount*self.values["EUR"]["USD"]["buy"],
            },
            {
                "name": "USD[EUR]",
                "description": "Convert USD to EUR",
                "dimension": "EUR",
                "value": usd_amount*self.values["USD"]["EUR"]["buy"],
            },
            {
                "name": "RUB[USD]",
                "description": "Convert RUB to USD",
                "dimension": "USD",
                "value": rub_amount/self.values["USD"]["RUB"]["sell"],
            },
            {
                "name": "RUB[USD]+EUR[USD]",
                "description": "Convert RUB and EUR to USD",
                "dimension": "USD",
                "value": rub_amount/self.values["USD"]["RUB"]["sell"] + eur_amount*self.values["EUR"]["USD"]["buy"],
            },
            {
                "name": "RUB[EUR]+USD[EUR]",
                "description": "Convert RUB and USD to EUR",
                "dimension": "EUR",
                "value": rub_amount/self.values["EUR"]["RUB"]["sell"] + usd_amount*self.values["USD"]["EUR"]["buy"],
            },
            {
                "name": "(EUR[USD]+USD)[RUB]",
                "description": "Total EUR and USD in USD",
                "dimension": "RUB",
                "value": (eur_amount*self.values["EUR"]["USD"]["buy"] + usd_amount)*self.values["USD"]["RUB"]["buy"],
            },
            {
                "name": "(USD[EUR]+EUR)[RUB]",
                "description": "Total EUR and USD in EUR",
                "dimension": "RUB",
                "value": (usd_amount*self.values["USD"]["EUR"]["buy"] + eur_amount)*self.values["EUR"]["RUB"]["buy"],
            },
        )
        for case in all_cases:
            if "value" in case:
                log.info("{} = {} {}".format(case["description"], round(case["value"], 3), case["dimension"]))
        log.info("")


if __name__ == "__main__":
    adviser = Adviser()
    adviser.help()
