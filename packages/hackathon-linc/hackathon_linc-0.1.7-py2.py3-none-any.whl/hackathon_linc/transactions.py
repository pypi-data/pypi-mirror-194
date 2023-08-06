# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 19:50:58 2021

@author: yasse
"""

import requests
from . import ipaddr as u
from typing import Union, Dict

# =============================================================================
# Buy, Sell, and Stoploss Securities
# =============================================================================


def _place_order(order_type: str, ticker: str, amount: int, price: Union[int, None] = None, days_to_cancel: int = 30) -> Dict:
    """
    This is a private function for placing buy, sell, and stoploss orders for securities.

    Args:
        order_type (str): The type of order (buy, sell, or stoploss)
        ticker (str): A security ticker (ex: STOCK1, STOCK2, etc.)
        amount (int): Number of shares
        price (int, optional): The price for which you want the security to be under in order to buy. If not specified, the order will be placed at the current price. Defaults to None.
        days_to_cancel (int, optional): How many days you want this trade to stay active: e.g entering 30 means that trade will be held for 30 days and then cancelled if security price never reaches given price to buy. Defaults to None.

    Returns:
        dict: The response content from the server as a dictionary
    """

    if not isinstance(amount, int) or (price is not None and not isinstance(price, int)) or (days_to_cancel is not None and not isinstance(days_to_cancel, int)):
        raise ValueError("""The amount and price must be integers""")

    params = {'type': order_type,
              'ticker': ticker,
              'amount': amount,
              'days_to_cancel': days_to_cancel}
    body = {'api_key': u.token}

    if price is not None:
        params['price'] = price

    url_s = u.url + '/order'

    response = requests.post(url_s, params=params, json=body)

    return response.json()


def buy(ticker: str, amount: int, price: Union[int, None] = None, days_to_cancel: int = 30) -> Dict:
    """
    This function places a buy order for a given security.

    Args:
        ticker (str): A security ticker (ex: STOCK1, STOCK2, etc.)
        amount (int): Number of shares
        price (int, optional): The price for which you want the security to be under in order to buy. If not specified, the order will be placed at the current price. Defaults to None.
        days_to_cancel (int, optional): How many days you want this trade to stay active: e.g entering 30 means that trade will be held for 30 days and then cancelled if security price never reaches given price to buy. Defaults to None.

    Returns:
        dict: The response content from the server as a dictionary
    """
    return _place_order('buy', ticker, amount, price, days_to_cancel)


def sell(ticker: str, amount: int, price: Union[int, None] = None, days_to_cancel: int = 30) -> Dict:
    """
    This function places a sell order for a given security.

    Args:
        ticker (str): A security ticker (ex: STOCK1, STOCK2, etc.)
        amount (int): Number of shares
        price (int, optional): The price for which you want the security to be under in order to buy. If not specified, the order will be placed at the current price. Defaults to None.
        days_to_cancel (int, optional): How many days you want this trade to stay active: e.g entering 30 means that trade will be held for 30 days and then cancelled if security price never reaches given price to buy. Defaults to None.

    Returns:
        dict: The response content from the server as a dictionary


    """
    return _place_order('sell', ticker, amount, price, days_to_cancel)


def stoploss(ticker: str, amount: int, price: float, days_to_cancel: int = 30):
    """
    This function places a stoploss order for a given security.

    Args:
        ticker (str): A security ticker (ex: STOCK1, STOCK2, etc.)
        amount (int): Number of shares
        price (float): The price for which you want the security to be under in order to buy. If not specified, the order will be placed at the current price. Defaults to None.
        days_to_cancel (int, optional): How many days you want this trade to stay active: e.g entering 30 means that trade will be held for 30 days and then cancelled if security price never reaches given price to buy. Defaults to None.

    Returns:
        dict: The response content from the server as a dictionary
    """
    return _place_order('stoploss', ticker, amount, price, days_to_cancel)


def cancel(order_id: Union[int, None] = None, ticker: Union[str, None] = None):
    """
    This function cancels a specific order or all orders for a given security.

    Args:
        order_id (int, optional): The id of the order you want to cancel. Defaults to None.
        ticker (str, optional): The ticker of the stock you want to cancel all orders for. Defaults to None.

    Returns:
        str: The response content from the server as a string
    """

    if order_id is None and ticker is None:
        raise ValueError("""You must specify either an order_id or a ticker""")

    params = {}
    if order_id is not None:
        params['order_id'] = order_id
    else:
        params['ticker'] = ticker

    url_s = u.url + '/cancel'
    body = {'api_key': u.token}

    response = requests.put(url_s, params=params, json=body)
    return response.json()
