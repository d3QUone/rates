__author__ = 'vladimir'

import json

import yaml
import requests

from logger import Logger

log = Logger("rates")


class Adviser(object):
    CATEGORY = "DebitCardsOperations"
    RUR_key = "RUB"
    USD_key = "USD"
    EUR_key = "EUR"
    ALL_CURRENCIES = (RUR_key, USD_key, EUR_key)
    COLORS = {
        'pink': '\033[95m',
        'blue': '\033[94m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'red': '\033[91m',
        'ENDC': '\033[0m',
        'bold': '\033[1m',
        'underline': '\033[4m'
    }

    def __init__(self):
        self.url = "https://www.tinkoff.ru/api/v1/currency_rates/"
        with open("config.yaml", "r") as f:
            self.config = yaml.load(f)
        self.rub_amount = self.config[self.RUR_key]
        self.usd_amount = self.config[self.USD_key]
        self.eur_amount = self.config[self.EUR_key]
        self.values = {}

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

    # TODO: fix text-log printout (save without color info)
    def str_color(self, color, data):
        """Colorize output"""
        return "%s%s%s" % (self.COLORS[color], data, self.COLORS['ENDC'])

    def help(self):
        """Calculate all variants"""
        self.__load_rates()

        all_amount_to_usd = (self.eur_amount * self.values[self.EUR_key][self.USD_key]["buy"] + self.usd_amount) * \
                            self.values[self.USD_key][self.RUR_key]["buy"]
        all_amount_to_eur = (self.usd_amount * self.values[self.USD_key][self.EUR_key]["buy"] + self.eur_amount) * \
                            self.values[self.EUR_key][self.RUR_key]["buy"]

        all_cases = (
            {
                "name": "EUR[RUB]",
                "description": "Convert EUR to RUB",
                "dimension": "RUB",
                "value": self.eur_amount * self.values[self.EUR_key][self.RUR_key]["buy"],
            },
            {
                "name": "USD[RUB]",
                "description": "Convert USD to RUB",
                "dimension": "RUB",
                "value": self.usd_amount * self.values[self.USD_key][self.RUR_key]["buy"],
            },
            {
                "name": "EUR[USD]",
                "description": "Convert EUR to USD",
                "dimension": "USD",
                "value": self.eur_amount * self.values[self.EUR_key][self.USD_key]["buy"],
            },
            {
                "name": "USD[EUR]",
                "description": "Convert USD to EUR",
                "dimension": "EUR",
                "value": self.usd_amount * self.values[self.USD_key][self.EUR_key]["buy"],
            },
            {
                "name": "RUB[USD]",
                "description": "Convert RUB to USD",
                "dimension": "USD",
                "value": self.rub_amount / self.values[self.USD_key][self.RUR_key]["sell"],
            },
            {
                "name": "RUB[USD]+EUR[USD]",
                "description": "Convert RUB and EUR to USD",
                "dimension": "USD",
                "value": self.rub_amount / self.values[self.USD_key][self.RUR_key]["sell"] +
                         self.eur_amount * self.values[self.EUR_key][self.USD_key]["buy"],
            },
            {
                "name": "RUB[EUR]+USD[EUR]",
                "description": "Convert RUB and USD to EUR",
                "dimension": "EUR",
                "value": self.rub_amount / self.values[self.EUR_key][self.RUR_key]["sell"] +
                         self.usd_amount * self.values[self.USD_key][self.EUR_key]["buy"],
            },
            {
                "name": "(EUR[USD]+USD)[RUB]",
                "description": "Total EUR and USD in USD",
                "dimension": "RUB",
                "value": all_amount_to_usd,
            },
            {
                "name": "(USD[EUR]+EUR)[RUB]",
                "description": "Total EUR and USD in EUR",
                "dimension": "RUB",
                "value": all_amount_to_eur,
            },
        )

        log.info("\n\n\tUSD: {} / {}\n\tEUR: {} / {}\n".format(
            self.str_color("green", self.values[self.USD_key][self.RUR_key]["buy"]),
            self.str_color("red", self.values[self.USD_key][self.RUR_key]["sell"]),
            self.str_color("green", self.values[self.EUR_key][self.RUR_key]["buy"]),
            self.str_color("red", self.values[self.EUR_key][self.RUR_key]["sell"]),
        ))
        for case in all_cases:
            if "value" in case and not ("disabled" in case and not case["disabled"]):
                log.info("{} = {} {}".format(
                    case["description"],
                    self.str_color("bold", round(case["value"], 3)),
                    self.str_color("blue", case["dimension"])
                ))

        # show profit
        if all_amount_to_usd > all_amount_to_eur:
            log.info("Move all into USD, profit now = {} {}".format(
                self.str_color("green", round(all_amount_to_usd - all_amount_to_eur, 1)),
                self.str_color("green", "RUR")
            ))
        else:
            log.info("Move all into EUR, profit now = {} {}".format(
                self.str_color("green", round(all_amount_to_eur - all_amount_to_usd, 1)),
                self.str_color("green", "RUR")
            ))


if __name__ == "__main__":
    adviser = Adviser()
    adviser.help()
