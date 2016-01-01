Tinkoff-Bank debit card rates and suggestions script

## Description

Скрипт работает с официальными курсами валют для дебетовых карт Тинькофф-банка, предлагает варианты арбитража. 

Лучше всего использовать в паре с https://tinkoffrates.ru

## Setup (global)

1) Install dependencies: `pip install -r requirements.txt`

2) Edit the `config.yaml` file with your money amount

3) Create the Alias to reach fast response in .bash_profile (OSX): type `nano ~/.bash_profile` and add `alias rates="cd path/to/rates/folder/ && python main.py"` where you must replace path/to/rates/folder/ with the real path.

## Setup (localized, recommended)

1) Create virtual environment in project folder: `virtualenv venv`

2) Install dependencies: `venv/bin/pip install -r requirements.txt`

3) Edit the `config.yaml` file with your money amount 

4) Create the Alias to reach fast response in .bash_profile (OSX): type `nano ~/.bash_profile` and add `alias rates="cd path/to/rates/folder/ && python main.py"` where you must replace path/to/rates/folder/ with the real path.

E.g. on my machine the command is: `alias rates="cd /Users/vladimir/Desktop/rates && venv/bin/python main.py"` and I launch this only by typing `rates`.

## Example output

```
2016-01-02 01:27:56,166 | INFO | Convert EUR to RUB = 78850.0 RUB
2016-01-02 01:27:56,167 | INFO | Convert USD to RUB = 72100.0 RUB
2016-01-02 01:27:56,167 | INFO | Convert EUR to USD = 1070.0 USD
2016-01-02 01:27:56,167 | INFO | Convert USD to EUR = 900.901 EUR
2016-01-02 01:27:56,167 | INFO | Convert RUB to USD = 133.245 USD
2016-01-02 01:27:56,167 | INFO | Convert RUB and EUR to USD = 1203.245 USD
2016-01-02 01:27:56,167 | INFO | Convert RUB and USD to EUR = 1022.778 EUR
2016-01-02 01:27:56,168 | INFO | Total EUR and USD in USD = 149247.0 RUB
2016-01-02 01:27:56,168 | INFO | Total EUR and USD in EUR = 149886.036 RUB
2016-01-02 01:27:56,168 | INFO | 
```

------

2016, Vladimir Kasatkin
