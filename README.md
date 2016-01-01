Tinkoff-Bank debit card rates and suggestions script

## Description

Скрипт работает с официальными курсами валют для дебетовых карт Тинькофф-банка, предлагает варианты арбитража. 

Лучше всего использовать в паре с https://tinkoffrates.ru

## Setup (global)

1) Install dependencies: `pip install -r requirements.txt`

2) Edit the `config.yaml` file with your money amount

3) Create the Alias to reach fast response: `alias rates="cd path/to/rates/folder/ && python main.py"` where you must 
replace path/to/rates/folder/ with the real path.

## Setup (localized, recommended)

1) Create virtual environment in project folder: `virtualenv venv`

2) Install dependencies: `venv/bin/pip install -r requirements.txt`

3) Edit the `config.yaml` file with your money amount 

4) Create the Alias to reach fast response: `alias rates="cd path/to/rates/folder/ && /path/to/venv/python main.py"` where you must 
replace path/to/rates/folder/ with the real path to the project and /path/to/venv/python with the real path to interpreter.

E.g. on my machine the command is: `alias rates="cd /Users/vladimir/Desktop/rates && venv/bin/python main.py"` and I launch this only by typing `rates`.

## Outputs

-

------

2016, Vladimir Kasatkin
