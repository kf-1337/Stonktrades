# this file contains all function to provide data gotten from data_getter.py towards dashboard, portfolio, orderhistory and watchlist

from .data_getter import *

def watchlist_per_user(user):
    return db_get_watchlist_per_user(user)

def portfolio_header_per_user(user):
    return db_get_portfolio_header(user)

def portfolio_data_per_user(user):
    return db_get_portfolio_data(user)

def orderhistory_per_user():
    return db_get_orderhistory()

def stonks_list_header():
    return db_get_stonks_list_header()

def stonks_list():
    return db_get_stonks_list()

