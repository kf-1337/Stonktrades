######################################################
# all the function to process the data first         #
# then the functions that call the api               #
# last the scheduler, that executes the functions    #
######################################################
# docs
# https://polygon.io/docs/stocks/get_v2_snapshot_locale_us_markets_stocks_tickers
# https://polygon-api-client.readthedocs.io/en/latest/Snapshot.html#get-all-snapshots

from datetime import datetime, timedelta, timezone
import time
from ..extensions import scheduler, db, client
from ..models import *
import csv

#######################################
#                                     #
# data process functions              #
#                                     #
#######################################

####################################################
# Pushing all available stonks to db "tickers"     #
####################################################

def push_ticker_list_to_db(ticker, name):
    print("Trigger: push_ticker_list_to_db")
    newentry = Tickerdetail(ticker=ticker, name = name)
    print("newentry created")       # to be deleted
    #with app.app_context():
    db.session.add(newentry)
    db.session.commit()
    print("DB Session commit")       # to be deleted

########################################################
# Pushing all available stonk details to db "Tickers"  #
########################################################

def push_ticker_details_to_db(ticker, address, city, postal_code, state, cik, composite_figi, currency_name, description, homepage_url, list_date, market_cap, name, primary_exchange, sic_code, sic_description, total_employees, type, weighted_shares_outstanding): # , locale, market
    print(datetime.now(),"Trigger: push_ticker_details_to_db", ticker)
    newentry = Tickerdetail(ticker=ticker, address=address, city=city, postal_code=postal_code, state=state, cik=cik, composite_figi=composite_figi, currency_name=currency_name,description=description, homepage_url=homepage_url, list_date=list_date, market_cap=market_cap, name=name, primary_exchange=primary_exchange, sic_code=sic_code, sic_description=sic_description, total_employees=total_employees, type=type, weighted_shares_outstanding=weighted_shares_outstanding) # locale=locale, market=market,
    db.session.add(newentry)
    db.session.commit()

########################################################
# Pushing ticker aggregates to db "pricehst"           #
########################################################

def push_ticker_aggs_to_db(timestamp, ticker, close):
    print("Trigger: push_ticker_aggs_to_db")
    newentry = PriceHst(timestamp = timestamp, ticker = ticker, close = close)
    db.session.add(newentry)
    db.session.commit()

####################################################
# Pushing all available stonks to db "tickers"     #
####################################################

def push_daily_aggs_to_db(date, ticker, close, high, low, transactions, open, volume, vwap):
    newentry = PriceHst(timestamp=date, ticker = ticker, close = close, high = high, low = low, ntrans = transactions, open = open, volume = volume, vwap = vwap)
    db.session.add(newentry)
    db.session.commit()


########################################################
# Pushing ticker list to file "ticker_list.txt"        #
########################################################

def push_ticker_list_to_file(ticker_list):
    print("Trigger: push_ticker_list_to_file")
    with open("ticker_list.txt", "a") as myfile:
        myfile.write(ticker_list)

########################################################
# Pushing ticker details to file "ticker_details.txt"  #
########################################################

def push_ticker_details_to_file(ticker_details):
    print("Trigger: push_ticker_list_to_file")
    with open("ticker_list.txt", "a") as myfile:
        myfile.write(ticker_details)

########################################################
# Pushing ticker aggregates to file "ticker_aggs.txt"  #
########################################################

def push_ticker_aggs_to_file(ticker_aggs):
    print("Trigger: push_ticker_list_to_file")
    with open("ticker_list.txt", "a") as myfile:
        myfile.write(ticker_aggs)



#######################################
#                                     #
# data get functions                  #
#                                     #
#######################################

#####################################################
# This is the api call to get all available tickers #
#####################################################

def job_ticker_list():
    print("Trigger: job_ticker_list")
    list_of_tickers = []
    for ticker in client.list_tickers(market="stocks", type="CS", active=True, limit=1000):
        print("Tickerdata arrived")
        push_ticker_list_to_db(ticker.ticker, ticker.name)
        # push_ticker_list(ticker)
        # print("Ticker data pushed to pusher.")
        list_of_tickers.append(ticker)
        # print (list_of_tickers)
        time.sleep(12)
    push_ticker_list_to_file(list_of_tickers)

######################################################
# This is the api call to get details to each ticker #
######################################################




def job_ticker_details(ticker):
    try:
        details = client.get_ticker_details(ticker=ticker)
        ticker = details.ticker if details.ticker is not None else ""
        if details.address is not None:
            address = details.address.address1 if details.address.address1 is not None else ""
            city = details.address.city if details.address.city is not None else ""
            postal_code = details.address.postal_code if details.address.postal_code is not None else ""
            state = details.address.state if details.address.state is not None else ""
        else:
            address = ""
            city = ""
            postal_code = ""
            state = ""
            
        cik = details.cik if details.cik is not None else ""
        composite_figi = details.composite_figi if details.composite_figi is not None else ""
        currency_name = details.currency_name if details.currency_name is not None else ""
        description = details.description if details.description is not None else ""
        homepage_url = details.homepage_url if details.homepage_url is not None else ""
        list_date = datetime.combine(datetime.strptime(details.list_date, "%Y-%m-%d"), datetime.min.time()) if details.list_date is not None else ""
        # locale = details.locale if details.locale is not None else ""
        # market = details.market if details.market is not None else ""
        market_cap = details.market_cap if details.market_cap is not None else ""
        name = details.name if details.name is not None else ""
        primary_exchange = details.primary_exchange if details.primary_exchange is not None else ""
        sic_code = details.sic_code if details.sic_code is not None else ""
        sic_description = details.sic_description if details.sic_description is not None else ""
        total_employees = details.total_employees if details.total_employees is not None else ""
        type = details.type if details.type is not None else ""
        weighted_shares_outstanding = details.weighted_shares_outstanding if details.weighted_shares_outstanding is not None else ""        
        push_ticker_details_to_db(ticker, address, city, postal_code, state, cik, composite_figi, currency_name, description, homepage_url, list_date, market_cap, name, primary_exchange, sic_code, sic_description, total_employees, type, weighted_shares_outstanding) #  locale, market,
    except:
        print(ticker)
    time.sleep(12)

def temp_job():
    with open('pricehstlist_only_tickers.csv', newline='') as tickercsv:
        csvreader = csv.reader(tickercsv, delimiter=',')
        for row in csvreader:
            ticker = row[0]
            job_ticker_details(ticker)


####################################################
# This is the api call for the ticker data per day #
####################################################

def job_ticker_aggs(ticker):
    print("Trigger: job_ticker_aggs")
    today = datetime.now()
    yesterday = datetime.now() + timedelta(days=-1)
    print("Dates:", yesterday,"->", today)
    aggs = []
    for a in client.list_aggs(
        ticker,
        1,
        "day",
        yesterday,
        today,
        limit=5000):
        aggs.append(a)
        push_ticker_aggs_to_db(a.timestamp, ticker, a.close)
    push_ticker_aggs_to_file(aggs)
    print(aggs)

##########################################################
# This is the api call for the daily ticker data per day #
##########################################################

def job_ticker_grouped_daily(amount_of_days = 10):
    tickerlist = []
    with open('tickers.csv', newline='') as tickercsv:
        csvreader = csv.reader(tickercsv, delimiter=',')
        for row in csvreader:
            tickerlist.append(row[0])
    print(tickerlist)
    startday = datetime.now()
    rangedays = []
    for rangeday in range(amount_of_days):
        date = (startday - timedelta(days = rangeday +2)).date().isoformat()
        rangedays.append(date)
    print(rangedays)
    for item in rangedays:
        print("Begin for Date: ", item)
        grouped = client.get_grouped_daily_aggs(
        item,
        #'2024-02-20',
        adjusted=True,
        market_type='stocks'
        )
        print("Data received")
        for ticker in grouped:
            if ticker.ticker in tickerlist:
                date = datetime.fromtimestamp(ticker.timestamp/1000.0)
                #print("Loop Ticker: ", ticker.ticker)
                # print(date, ticker.ticker, ticker.close, ticker.high, ticker.low, ticker.transactions, ticker.open, ticker.volume, ticker.vwap)
                push_daily_aggs_to_db(date, ticker.ticker, ticker.close, ticker.high, ticker.low, ticker.transactions, ticker.open, ticker.volume, ticker.vwap)
        print("End for Date: ", item)
        time.sleep(12)


#########################
# to test the scheduler #
#########################

def testing():
    print("This is a test for every 5 seconds.", datetime.now())


def testing2():
    print("This is a test for every minute.", datetime.now())

# scheduler.add_job(testing2, 'cron', minute = "*")
# scheduler.add_job(testing, 'cron', second = "*/5")


#######################################
#                                     #
# scheduler job manager               #
#                                     #
#######################################


exectime = datetime.now() + timedelta(seconds=10)
print(exectime, "is set")
scheduler.add_job(job_ticker_list, 'date', run_date = exectime)
#scheduler.add_job(job_ticker_list, 'cron', day = "*")