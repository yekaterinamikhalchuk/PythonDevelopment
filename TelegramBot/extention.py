import requests
import json
from config import keys


class APIException(Exception):
    pass

class CurrencyConverter:

    @staticmethod
    def get_price(cur_from: str, cur_to: str, amount: str):

        if cur_to == cur_from:
            raise APIException('The same values')
        try:
            cur_from_ticker = keys[cur_from]
        except KeyError:
            raise APIException('The currency is unknown')

        try:
            cur_to_ticker = keys[cur_to]
        except KeyError:
            raise APIException('The currency is unknown. To see available currencies press "Currencies available 💸"')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException('The value has the wrong type. To see input example press "Input example 🔎"')

        response = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={cur_from_ticker}&tsyms={cur_to_ticker}')
        amount_cur_to = (json.loads(response.content))[cur_to_ticker] * amount

        return amount_cur_to