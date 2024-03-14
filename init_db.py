from stonktrades import app
from app import db
from app.models import  *
from werkzeug.security import generate_password_hash
import csv

with app.app_context():
    db.drop_all()
    db.create_all()
    print("Importing Tickerdetails...")
    with open('tickerdetails.csv', newline='') as tickerdetailscsv:
        csvreader = csv.reader(tickerdetailscsv, delimiter=',')
        formatdate = '%Y-%m-%d %H:%M:%S'
        for row in csvreader:
            entry = datetime.strptime(row[11], formatdate)
            rowdata = Tickerdetail(ticker = row[0], address = row[1], city=row[2], postal_code=row[3], state=row[4], cik=row[5], composite_figi=row[6], currency_name = row[7], description = row[9], homepage_url = row[10], list_date = entry, market_cap = row[12], name = row[13], primary_exchange = row[14], sic_code = row[15], sic_description = row[16], total_employees = row[17], type = row[18], weighted_shares_outstanding = row[19])
            db.session.add(rowdata)
        db.session.commit()
    print("Tickerdetails imported.")
    print("Importing Pricehistory...( 130.000 entries maybe take a minute)")

    with open('pricehstlist.csv', newline='') as pricehstlistcsv:
        csvreader = csv.reader(pricehstlistcsv, delimiter=',')
        formatdate = '%Y-%m-%d %H:%M:%S'
        for row in csvreader:
            entry = datetime.strptime(row[1], formatdate)
            rowdata = PriceHst(timestamp = entry, ticker = row[2], close = row[3], high = row[4], low = row[5], ntrans = row[6], open = row[7], volume =row[8], vwap = row[9])
            db.session.add(rowdata)
        db.session.commit()
    print("Pricehistory imported.")



    print("Create User...")
    admin_user = User(username='admin', password=generate_password_hash('password', method='pbkdf2', salt_length=16), role="Admin")
    user_user = User(username='user', password=generate_password_hash('password', method='pbkdf2', salt_length=16), role="User")
    db.session.add(admin_user)
    db.session.add(user_user)    
    db.session.commit()
    print("Admin and User created.")