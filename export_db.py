from stonktrades import app
from app.models import Ticker, PriceHst, Tickerdetail
from app import db
import csv


########################################################################
# This file contains helpfull snippets to export DB data to csv.       #
# Uncomment the one you want to use, run it, then comment it out again.#
########################################################################


########################################################################
# With this you will export a csv list of all ticker for further use.  #
# Usefull if you have to rebuild the DB..                              #
########################################################################


# with app.app_context():
#     tickerlist = db.session.query(Tickerdetail.ticker).all()
#     with open('tickers.csv', 'w', newline='') as tickercsv:
#         csvwriter = csv.writer(tickercsv, delimiter=',')
#         csvwriter.writerow(["ticker"])
#         for item in tickerlist:
#             csvwriter.writerow([item.ticker])

########################################################################
# With this you will export the PriceHst table with all data.          #
# Usefull if you have to rebuild the DB..                              #
########################################################################

# with app.app_context():
#     pricehstlist = db.session.query(PriceHst).all()
#     with open('pricehstlist.csv', 'w', newline='') as tickercsv:
#         csvwriter = csv.writer(tickercsv, delimiter=',')
#         csvwriter.writerow(["id", "timestamp", "ticker", "close", "high", "low", "ntrans", "open", "volume", "vwap"])
#         for item in pricehstlist:
#             csvwriter.writerow([item.id, item.timestamp, item.ticker, item.close, item.high, item.low, item.ntrans, item.open, item.volume, item.vwap])


########################################################################
# With this you will export a csv list of all tickers in pricehst.     #
# Usefull if you want to compare this to the tickerdetails list.       #
# Or when you have to rebuild the DB..                                 #
########################################################################

# with app.app_context():
#     pricehstlist_only_tickers = db.session.query(PriceHst.ticker).group_by(PriceHst.ticker).all()
#     with open('pricehstlist_only_tickers.csv', 'w', newline='') as tickercsv:
#         csvwriter = csv.writer(tickercsv, delimiter=',')
#         csvwriter.writerow(["ticker"])
#         for item in pricehstlist_only_tickers:
#             csvwriter.writerow([item.ticker])

########################################################################
# With this you will export a csv list of the table tickerdetails.     #
# Usefull if you have to rebuild the DB..                              #
########################################################################


# with app.app_context():
#     tickerdetailslist = db.session.query(Tickerdetail).all()
#     with open('tickerdetails.csv', 'w', newline='') as tickerdetailscsv:
#         csvwriter = csv.writer(tickerdetailscsv, delimiter=',')
#         #csvwriter.writerow(["ticker", "address", "city", "postal_code", "state", "cik", "composite_figi", "currency_name", "delisted_utc", "description", "homepage_url","list_date", "locale", "market", "market_cap", "name", "primary_exchange", "sic_code", "sic_description", "total_employees", "type", "weighted_shares_outstanding"])
#         for item in tickerdetailslist:
#             csvwriter.writerow([item.ticker, item.address, item.city, item.postal_code, item.state, item.cik, item.composite_figi, item.currency_name, item.description, item.homepage_url, item.list_date, item.locale, item.market,  item.market_cap, item.name, item.primary_exchange, item.sic_code, item.sic_description, item.total_employees, item.type, item.weighted_shares_outstanding])

