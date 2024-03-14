from flask import render_template, request, redirect, flash
from flask_login import login_required, current_user
from . import dpow
from app.api.json_formatter import *
from app.api.data_formatter import *
from .forms import *
from ..models import Tickerdetail, Transaction, PriceHst
from ..extensions import db
# from wtforms_alchemy import QuerySelectMultipleField


# htmx request goes here
@dpow.route('/searchbar')
@login_required
def searchbar():
    q = request.args.get("q")
    print("Trigger:", q)
    if q:
        results = Tickerdetail.query.filter(Tickerdetail.ticker.icontains(q) | Tickerdetail.name.icontains(q)).order_by(Tickerdetail.ticker.asc()).limit(5).all()
        print(results)
    else:
        results = []
    return render_template("searchbar_result.html", results = results)

# left navbar goes here
@dpow.route('/dashboard')
@login_required
def test():
    return render_template('dashboard.html', pageTitle='Dashboard', name=current_user.username)

# left navbar goes here
@dpow.route('/portfolio')
@login_required
def portfolio():
    portfolio_header = portfolio_header_per_user(current_user.username)
    portfolio_data = portfolio_data_per_user(current_user.username)

    return render_template('portfolio.html', pageTitle='Portfolio', name=current_user.username, portfolio_header = portfolio_header, portfolio_data = portfolio_data)

# left navbar goes here
@dpow.route('/orderhistory')
@login_required
def orderhistory():
    orderhistory_header = ['Timestamp', 'Ticker','Price','Transactiontype']
    orderhistory = orderhistory_per_user()
    return render_template('orderhistory.html', pageTitle='Orderhistory', name=current_user.username, orderhistory = orderhistory, orderhistory_header = orderhistory_header)

# left navbar goes here
@dpow.route('/watchlist')
@login_required
def watchlist():
    watchlist=watchlist_per_user(current_user.username)
    print(watchlist)
    return render_template('watchlist.html', pageTitle='Watchlist', watchlist = watchlist, name=current_user.username)

# no direkt link goes here. but if User looks it up. Loadtime is bad though.
@dpow.route('/stonks')
@login_required
def stonktable():
    stonks_header_list = stonks_list_header()
    stonksdetails_list = stonks_list()    
    return render_template('stonkstable.html', pageTitle = 'Stonks', name=current_user.username, stonks_header_list = stonks_header_list, stonksdetails_list = stonksdetails_list)


# Every link of a ticker goes to each subpage
@dpow.route('/stonks/<ticker>', methods=['GET', 'POST'])
@login_required
def stonks(ticker):
    formarg = request.args.get('form', default=None, type=None)
    print("Formargs: ", formarg)
    user = User.query.filter(User.username == current_user.username).first()
    formwatchlist = WatchlistForm(data={"watchlist": user.watchlistentries})
    formwatchlist.watchlist.query = Tickerdetail.query.filter_by(ticker = ticker).all()
    formbuy = BuyForm()
    formsell = SellForm()
    renderstonkdata = Tickerdetail.query.filter(Tickerdetail.ticker == ticker).first()
    if request.method == 'GET':
        return render_template('stonks.html', pageTitle = ticker, name=current_user.username, stonk = ticker, formwatchlist = formwatchlist, formbuy=formbuy, formsell = formsell, renderstonkdata = renderstonkdata)
    if request.method == 'POST':
        print("Trigger: Post method on watchlist, buy, or sell.")
        if formarg == "buy" and formbuy.validate_on_submit():
            print("Trigger: Formbuy ")
            amount = formbuy.amount.data
            print(amount)
            currentprice = PriceHst.query.filter(PriceHst.ticker == ticker).order_by(PriceHst.timestamp.desc()).first()
            for number in range(0, amount):
                print(number)
                newtransaction = Transaction(price = currentprice.close, trantype = "BUY" , ticker = ticker, username = current_user.username)
                db.session.add(newtransaction)
                # user.transactions.extend(newtransaction[0])
            db.session.commit()
            temp = f"/stonks/{ticker}"
            flash('Bought stonk.')
            return redirect(temp)
        elif formarg == "sell" and formsell.validate_on_submit():
            # Check if user has those assets has to be implemented here.
            print("Trigger: Formsell ")
            amount = formsell.amount.data
            print(amount)
            currentprice = PriceHst.query.filter(PriceHst.ticker == ticker).order_by(PriceHst.timestamp.desc()).first()
            for number in range(0, amount):
                print(number)
                newtransaction = Transaction(price = currentprice.close, trantype = "SELL" , ticker = ticker, username = current_user.username)
                db.session.add(newtransaction)
            db.session.commit()
            temp = f"/stonks/{ticker}"
            flash('Sold stonk.')
            return redirect(temp)
        elif formarg == "watchlist" and formwatchlist.validate_on_submit():
            print("Trigger: Formwatchlist")
            tempvalue = Tickerdetail.query.filter_by(ticker = ticker).all()
            type(formwatchlist.watchlist.data)
            type(user.watchlistentries)
            if tempvalue[0] in user.watchlistentries:
                user.watchlistentries.remove(tempvalue[0])
            user.watchlistentries.extend(formwatchlist.watchlist.data)
            db.session.commit()
            temp = f"/stonks/{ticker}"
            return redirect(temp)
        else:
            print("Error: ", formbuy.amount.data, formsell.amount.data)
            print("Error in Buy/Sell form for user: ", current_user.username)
    return render_template('stonks.html', pageTitle = ticker, name=current_user.username, stonk = ticker, formwatchlist = formwatchlist, formbuy=formbuy, formsell = formsell, renderstonkdata = renderstonkdata) 



@dpow.route('/api/get_topx_data/')
@login_required
def api_topx():
    x = request.args.get('x', default = 2, type = int)
    return dashboard_topX(x)

@dpow.route('/api/get_dash_over_time_data/')
@login_required
def api_dash_over_time():
    y = request.args.get('y', default = "1m", type = str)
    return dash_dash_over_time(y)



@dpow.route('/dpow/gtcs')
@login_required
def gtcs_dpow():
    return render_template('gtcs_dpow.html', pageTitle="GTCs", name=current_user.username)


@dpow.route('/dpow/imprint')
@login_required
def imprint_dpow():
    return render_template('imprint_dpow.html', pageTitle="Imprint", name=current_user.username)

@dpow.route('/dpow/gdpr')
@login_required
def gdpr_dpow():
    return render_template('gdpr_dpow.html', pageTitle="GDPR", name=current_user.username)
