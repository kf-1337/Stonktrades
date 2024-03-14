# this file contains all functions to access the db and providing data to the formatters
from flask_login import current_user
from sqlalchemy import func
import sqlite3
from pathlib import Path
from ..extensions import db
from ..models import *
from datetime import datetime, timedelta, timezone


def db_get_topx(x):
    print('db_accessX=',x)
    dict_to_sort = db_get_topall()
    #print(dict_to_sort)
    sorted_topx_without_rest = dict(sorted(dict_to_sort.items(), key = lambda x:x[1], reverse=True)[:x])
    #print(sorted_topx_without_rest)
    sorted_topx = dict(sorted(dict_to_sort.items(), key = lambda x:x[1], reverse=True))
    rest = 0
    temp1 = round(sum(sorted_topx_without_rest.values()),2)
    #print(temp1)
    
    rest = sum(sorted_topx.values()) - temp1
    sorted_topx_without_rest.update({"Rest": rest})
    return sorted_topx_without_rest
    


def db_get_topall():
    dictreturn = {}
    list_of_assets = []
    assets = Transaction.query.filter(Transaction.username == current_user.username).all()
    for asset in assets:
        if asset.ticker not in list_of_assets:
            list_of_assets.append(asset.ticker)
    for stonk in list_of_assets:
        objects_of_asset = Transaction.query.filter(Transaction.ticker == stonk).all()
        count_of_asset = 0
        count_of_buy = 0
        count_of_sell = 0
        amount_invested_in_asset = 0.0
        amount_put_in_overall = 0.0
        amount_got_out_overall = 0.0
        profit_per_asset = 0.0
        current_price_objects = PriceHst.query.filter(PriceHst.ticker == stonk).order_by(PriceHst.timestamp.desc()).first()
        current_price = current_price_objects.close
        
        for entry in objects_of_asset:
            if entry.trantype == "BUY":
                count_of_asset = count_of_asset + 1
                count_of_buy = count_of_buy + 1
                amount_invested_in_asset = amount_invested_in_asset + entry.price
                amount_put_in_overall = amount_put_in_overall + entry.price
            elif entry.trantype == "SELL":
                count_of_asset = count_of_asset - 1
                count_of_sell = count_of_sell + 1
                amount_invested_in_asset = amount_invested_in_asset - entry.price
                amount_got_out_overall = amount_got_out_overall + entry.price
            else:
                print("Error in transactions table. TranType neither buy nor sell")
        if count_of_asset > 0:
            stock_value = count_of_asset * current_price
            tempdata = {str(stonk): stock_value}
            dictreturn.update(tempdata)
        
    #print(dictreturn)
    return dictreturn







def db_get_dash_over_time(y):
    print('db_accessY=',y)
    if y == "1w":
        dayrange = 7
    elif y == "1m":
        dayrange = 30
    elif y == "3m":
        dayrange = 90
    elif y == "6m":
        dayrange = 180
    elif y == "1y":
        dayrange = 365
    else:
        dayrange = 30
    
    earlistdate = datetime.now() - timedelta(days = dayrange)
    #print(earlistdate)

    dictreturn = {}


    for i in range(0,dayrange):
        per_day_date = earlistdate + timedelta(days = i)
        per_day_total_sum = 0
        #print(per_day_date)
        ################################data = Transaction.query.filter(Transaction.username == current_user.username, Transaction.transaction_timestamp <= per_day_date).all()
        list_of_assets = []
        assets = Transaction.query.filter(Transaction.username == current_user.username, Transaction.transaction_timestamp <= per_day_date).all()
        for asset in assets:
            if asset.ticker not in list_of_assets:
                list_of_assets.append(asset.ticker)
        for stonk in list_of_assets:
            objects_of_asset = Transaction.query.filter(Transaction.ticker == stonk, Transaction.transaction_timestamp <= per_day_date).all()
            count_of_asset = 0
            count_of_buy = 0
            count_of_sell = 0
            amount_invested_in_asset = 0.0
            amount_put_in_overall = 0.0
            amount_got_out_overall = 0.0
            profit_per_asset = 0.0
            current_price_objects = PriceHst.query.filter(PriceHst.ticker == stonk, PriceHst.timestamp <= per_day_date).order_by(PriceHst.timestamp.desc()).first()
            current_price = current_price_objects.close
            
            for entry in objects_of_asset:
                if entry.trantype == "BUY":
                    count_of_asset = count_of_asset + 1
                    count_of_buy = count_of_buy + 1
                    amount_invested_in_asset = amount_invested_in_asset + entry.price
                    amount_put_in_overall = amount_put_in_overall + entry.price
                elif entry.trantype == "SELL":
                    count_of_asset = count_of_asset - 1
                    count_of_sell = count_of_sell + 1
                    amount_invested_in_asset = amount_invested_in_asset - entry.price
                    amount_got_out_overall = amount_got_out_overall + entry.price
                else:
                    print("Error in transactions table. TranType neither buy nor sell")
            if count_of_asset > 0:
                amount_worth_per_day_per_stonk = current_price * count_of_asset if count_of_asset > 0 else 1

            per_day_total_sum = per_day_total_sum + amount_worth_per_day_per_stonk
        

    
        tempdata = {str(per_day_date): str(per_day_total_sum)}
        dictreturn.update(tempdata)
    #print(dictreturn)
    return dictreturn











def db_get_watchlist_per_user(user):
    print('Trigger: db_accessWatchlist=',user)
    print(current_user.username)
    watchlist_entries = []
    print(current_user.watchlistentries)
    for item in current_user.watchlistentries:
        print(current_user.watchlistentries)
        get_watchlist_entry = Tickerdetail.query.filter(Tickerdetail.ticker == item.ticker).first()
        print(get_watchlist_entry)
        get_pricehst_entries = PriceHst.query.filter(PriceHst.ticker == item.ticker).all()
        oneweekago_date = datetime.now() - timedelta(days = 7)
        onemonthago_date = datetime.now() - timedelta(days = 30)
        threemonthsago_date = datetime.now() - timedelta(days = 90)
        sixmonthsago_date = datetime.now() - timedelta(days = 180)
        oneyearago_date = datetime.now() - timedelta(days = 365)
        
        today = PriceHst.query.filter(PriceHst.ticker == item.ticker).order_by(PriceHst.timestamp.desc()).first()
        oneweekago = PriceHst.query.filter(PriceHst.timestamp <= oneweekago_date, PriceHst.ticker == item.ticker).order_by(PriceHst.timestamp.desc()).first()
        onemonthago = PriceHst.query.filter(PriceHst.timestamp <= onemonthago_date, PriceHst.ticker == item.ticker).order_by(PriceHst.timestamp.desc()).first()
        threemonthsago = PriceHst.query.filter(PriceHst.timestamp <= threemonthsago_date, PriceHst.ticker == item.ticker).order_by(PriceHst.timestamp.desc()).first()
        sixmonthsago = PriceHst.query.filter(PriceHst.timestamp <= sixmonthsago_date, PriceHst.ticker == item.ticker).order_by(PriceHst.timestamp.desc()).first()
        oneyearago = PriceHst.query.filter(PriceHst.timestamp <= oneyearago_date, PriceHst.ticker == item.ticker).order_by(PriceHst.timestamp.desc()).first()
        
        oneweekdiff = today.close / oneweekago.close
        onemonthdiff = today.close / onemonthago.close
        threemonthsdiff = today.close / threemonthsago.close        
        sixmonthsdiff = today.close / sixmonthsago.close
        oneyeardiff = today.close / oneyearago.close        
        
        dictentry = {'ticker': get_watchlist_entry.ticker, 'name':get_watchlist_entry.name, 'today': today.close, 'oneweekdiff': round(oneweekdiff,2),'onemonthdiff': round(onemonthdiff,2),'threemonthsdiff': round(threemonthsdiff,2),'sixmonthsdiff': round(sixmonthsdiff,2),'oneyeardiff': round(oneyeardiff,2)}
        #print(dictentry)
        watchlist_entries.append(dictentry)
    return watchlist_entries







def db_get_portfolio_header(user):
    return ["Stonk", "Number of Shares", "Total invested in $", "Avg. Buy", "Avg. Sell", "Performance in $", "Performance in %"]

def db_get_portfolio_data(user):
    print("Trigger: db_get_portfolio_data")
    portfolio_entries = []
    
    list_of_assets = []
    assets = Transaction.query.filter(Transaction.username == current_user.username).all()
    for asset in assets:
        if asset.ticker not in list_of_assets:
            list_of_assets.append(asset.ticker)
    print("Portfolio being build for: ", list_of_assets)
    for stonk in list_of_assets:
        objects_of_asset = Transaction.query.filter(Transaction.ticker == stonk).all()
        count_of_asset = 0
        count_of_buy = 0
        count_of_sell = 0
        amount_invested_in_asset = 0.0
        amount_put_in_overall = 0.0
        amount_got_out_overall = 0.0
        profit_per_asset = 0.0
        current_price_objects = PriceHst.query.filter(PriceHst.ticker == stonk).order_by(PriceHst.timestamp.desc()).first()
        current_price = current_price_objects.close
        
        for entry in objects_of_asset:
            if entry.trantype == "BUY":
                count_of_asset = count_of_asset + 1
                count_of_buy = count_of_buy + 1
                amount_invested_in_asset = amount_invested_in_asset + entry.price
                amount_put_in_overall = amount_put_in_overall + entry.price
            elif entry.trantype == "SELL":
                count_of_asset = count_of_asset - 1
                count_of_sell = count_of_sell + 1
                amount_invested_in_asset = amount_invested_in_asset - entry.price
                amount_got_out_overall = amount_got_out_overall + entry.price
            else:
                print("Error in transactions table. TranType neither buy nor sell")
        if count_of_asset > 0:
            amount_worth_now = current_price * count_of_asset if count_of_asset > 0 else 1
            profit_per_asset_percent = amount_worth_now / amount_invested_in_asset if amount_invested_in_asset > 0 else 1 # performance total in %
            profit_per_asset_total = amount_worth_now - amount_invested_in_asset   # Profit in $ 
            avgbuy = amount_put_in_overall / count_of_buy if count_of_buy > 0 else 1
            if count_of_sell > 0:
                avgsell = round(amount_got_out_overall / count_of_sell,2)
            else:
                avgsell = "no sell yet"
            dictentry = {'ticker': stonk, 'holdingamount': round(count_of_asset,2),'invested': round(amount_invested_in_asset,2), 'avgbuy': round(avgbuy, 2), 'avgsell': avgsell, 'profittotal': round(profit_per_asset_total, 2), 'profitperc': round(profit_per_asset_percent, 2)}
            portfolio_entries.append(dictentry)
    
    return portfolio_entries


    
def db_get_orderhistory():
    orderhistory_entries = []
    for item in current_user.transactions:
        dictentry = {'timestamp': item.transaction_timestamp,'ticker': item.ticker, 'price': item.price, 'trantype': item.trantype}
        orderhistory_entries.append(dictentry)
    return orderhistory_entries


def db_get_stonks_list_header():
    stonks_header_list = ['Ticker', 'Name', 'Price']
    return stonks_header_list

def db_get_stonks_list():
    print("Trigger: db_get_stonks_list")
        # Tickerdetail.metadata.tables['tickerdetails'].columns.keys()
    stonksdetails_list = []
    alltickerdetailslist = Tickerdetail.query.all()
    for d in alltickerdetailslist:
        x = d.__dict__
        y = PriceHst.query.filter_by(ticker = x['ticker']).order_by(PriceHst.timestamp.desc()).first()
        price = y.__dict__
        stonksdetails_list.append([x['ticker'], x['name'], price['close']])
    # print( stonksdetails_list)
    return stonksdetails_list



def db_get_stonk_chart(y, s):
    print('Trigger: db_get_stonk_chart y=',y, 's=', s)
    if y == "1w":
        dayrange = 7
    elif y == "1m":
        dayrange = 30
    elif y == "3m":
        dayrange = 90
    elif y == "6m":
        dayrange = 180
    elif y == "1y":
        dayrange = 365
    else:
        dayrange = 30
        
    earlistdate = datetime.now() - timedelta(days = dayrange)
    #print(earlistdate)
    

    result = PriceHst.query.filter(PriceHst.ticker == s, PriceHst.timestamp > earlistdate).order_by(PriceHst.timestamp.asc()).all()
    
    dictreturn = {}
    for row in result:
        if row.timestamp is not None and row.close is not None:
            tempdata = {str(row.timestamp): row.close}
            dictreturn.update(tempdata)
    #print(dictreturn)
    return dictreturn
        # print(row.timestamp, row.close)


    
    
    # engine = create_engine(rf'sqlite:///database.sqlite')
    # session = Session(engine)
    
    # pricehst = Table('pricehst')
    # ticker = s
    
    
    
    # q = Query.from_(pricehst).where(pricehst.ticker == ticker).orderby(pricehst.timestamp, order=Order.desc).select(pricehst.timestamp, pricehst.close,).limit(dayrange)
    # print(q)
    
    # result = session.execute(q)
    
    # print(result)
    
    
    

