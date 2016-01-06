__author__ = 'vladimir'

import sys
import json

import yaml
import requests

from logger import Logger

log = Logger("rates")


class Adviser(object):
    URL = "https://www.tinkoff.ru/api/v1/currency_rates/"
    CATEGORY = "DebitCardsTransfers"
    RUR_key = "RUB"
    USD_key = "USD"
    EUR_key = "EUR"
    ALL_CURRENCIES = (RUR_key, USD_key, EUR_key)

    def __init__(self):
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
            data = requests.get(self.URL).json()
            self.__filter_data(data["payload"]["rates"])
        except Exception as e:
            log.error("load_rates error: {}".format(repr(e)))

    def show_available(self):
        return "{} RUR, {} USD, {} EUR".format(
            Logger.colorize("green" if self.rub_amount > 0 else "red", self.rub_amount),
            Logger.colorize("green" if self.usd_amount > 0 else "red", self.usd_amount),
            Logger.colorize("green" if self.eur_amount > 0 else "red", self.eur_amount),
        )

    def get(self, args):
        if len(args) == 4:
            _, _, amount, currency = args
            if currency not in self.ALL_CURRENCIES:
                log.error("Currency {} is not supported".format(
                    Logger.colorize("blue", currency)
                ))
                return
        elif len(args) == 3:
            _, _, amount = args
            currency = self.RUR_key
            log.info("No currency was provided, using {} by default".format(
                Logger.colorize("blue", currency)
            ))
        else:
            log.error("Usage: {} {}".format(
                Logger.colorize("green", "get"),
                Logger.colorize("red", "amount [currency]")
            ))
            return

        s = "\n\n\t{}".format(self.show_available())

        log.info(s)

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
                "dimension": "RUB\n",
                "value": self.usd_amount * self.values[self.USD_key][self.RUR_key]["buy"],
            },
            {
                "name": "EUR[USD]",
                "description": "Convert EUR to USD",
                "dimension": "USD",
                "value": self.eur_amount * self.values[self.EUR_key][self.USD_key]["buy"],
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
                "dimension": "USD\n",
                "value": self.rub_amount / self.values[self.USD_key][self.RUR_key]["sell"] +
                         self.eur_amount * self.values[self.EUR_key][self.USD_key]["buy"],
            },
            # TODO: add total in usd
            {
                "name": "USD[EUR]",
                "description": "Convert USD to EUR",
                "dimension": "EUR",
                "value": self.usd_amount * self.values[self.USD_key][self.EUR_key]["buy"],
            },
            {
                "name": "RUB[EUR]",
                "description": "Convert RUB to EUR",
                "dimension": "EUR",
                "value": self.rub_amount / self.values[self.EUR_key][self.RUR_key]["sell"],
            },
            {
                "name": "RUB[EUR]+USD[EUR]",
                "description": "Convert RUB and USD to EUR",
                "dimension": "EUR\n",
                "value": self.rub_amount / self.values[self.EUR_key][self.RUR_key]["sell"] +
                         self.usd_amount * self.values[self.USD_key][self.EUR_key]["buy"],
            },
            # TODO: add total in eur
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
        
        s = "\n\n\t{}\n\n\tUSD/RUR: {} / {}\n\tEUR/RUR: {} / {}\n\n".format(
            self.show_available(),
            Logger.colorize("green", self.values[self.USD_key][self.RUR_key]["buy"]),
            Logger.colorize("red", self.values[self.USD_key][self.RUR_key]["sell"]),
            Logger.colorize("green", self.values[self.EUR_key][self.RUR_key]["buy"]),
            Logger.colorize("red", self.values[self.EUR_key][self.RUR_key]["sell"]),
        )
        for case in all_cases:
            if "value" in case and not ("disabled" in case and not case["disabled"]):
                s += "{} = {} {}\n".format(
                    case["description"],
                    Logger.colorize("bold", round(case["value"], 3)),
                    Logger.colorize("blue", case["dimension"])
                )
        # show profit
        if all_amount_to_usd > all_amount_to_eur:
            s += "If move all into {} profit = {} {}\n".format(
                Logger.colorize("green", "USD"),
                Logger.colorize("green", round(all_amount_to_usd - all_amount_to_eur, 1)),
                Logger.colorize("green", "RUR")
            )
        else:
            s += "If move all into {} profit = {} {}\n".format(
                Logger.colorize("green", "EUR"),
                Logger.colorize("green", round(all_amount_to_eur - all_amount_to_usd, 1)),
                Logger.colorize("green", "RUR")
            )
        s += "=" * 50
        log.info(s)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
    else:
        command = None

    adviser = Adviser()
    if not command:
        adviser.help()
    elif command == "get":
        adviser.get(sys.argv)
    else:
        log.error("Command {} is not available".format(Logger.colorize("red", command)))
