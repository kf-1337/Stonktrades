from flask_login import UserMixin, current_user
from .extensions import db
from datetime import datetime


# This was my try of a role bases autorization. Currently the role is in the userobject.

# class Role(db.Model):
#     __tablename__= "roles"
#     id = db.Column(db.Integer, primary_key=True)
#     rolename = db.Column(db.String(25), unique=True, nullable=False, default='User')
#     users = db.relationship('User', backref='rolename', lazy=True)

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(25), nullable=False, default='User') # could be replaces with role = db.relationship("Role", back_populates="users")
    watchlistentries = db.relationship("Tickerdetail", secondary="userwatchlist", back_populates="users")
    transactions = db.relationship("Transaction", back_populates="user")
    
    
    def __repr__(self):
        return f"<User: {self.username}>"
    
    def __str__(self):
        return self.username




# THis was my try on a wallet system. That a user could have more than one Wallet...

# class Wallet(db.Model):
#     __tablename__ = "wallets"
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     transactions = db.relationship("Transaction")

class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    transaction_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    price = db.Column(db.Integer, nullable=False)
    trantype = db.Column(db.String(4), nullable=False)  # either buy or sell
    ticker = db.Column(db.String(10), nullable=False)
    username = db.Column(db.Integer, db.ForeignKey('users.username'), nullable=False)
    user = db.relationship("User", back_populates="transactions")
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, timestamp={self.transaction_timestamp},price={self.price},ticker={self.ticker})"



# This was my try on a asset based transaction. As you could also sell singulare assets, when you order a bunch in one transaction
# Now i just itterate over the amount of the buy form and create multiple transactions

# class Asset(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     buy_timestamp = db.Column(db.Integer, nullable=False)
#     buyprice = db.Column(db.Integer, nullable=False)
#     ticker = db.Column(db.String(10))
#     transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=False)
    
#     def __repr__(self):
#         return f"<Asset(id={self.id}, timestamp='{self.buy_timestamp}, ticker='{self.ticker}')>"
    

class PriceHst(db.Model):
    __tablename__ = "pricehst"
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    ticker = db.Column(db.String(10))    # Future improvement: Replace with relationship
    close = db.Column(db.Integer)
    high = db.Column(db.Integer)
    low = db.Column(db.Integer)
    ntrans = db.Column(db.Integer)
    open = db.Column(db.Integer)
    volume = db.Column(db.Integer)
    vwap = db.Column(db.Integer)
    
    def __repr__(self):
        return f"<PriceHst-Object: {self.ticker}>"
    
class Tickerdetail(db.Model):
    __tablename__ = "tickerdetails"
    id = db.Column(db.Integer, primary_key=True)    
    ticker = db.Column(db.String(10),unique=True)
    address = db.Column(db.String(100))
    city = db.Column(db.String(100))
    postal_code = db.Column(db.Integer)
    state = db.Column(db.String(4))
    cik = db.Column(db.Integer)
    composite_figi = db.Column(db.String(15))
    currency_name = db.Column(db.String(6))
    # delisted_utc = db.Column(db.DateTime)     got problems with None objects
    description = db.Column(db.Text)
    homepage_url = db.Column(db.String(50))
    list_date = db.Column(db.DateTime)
    locale = db.Column(db.Enum)
    market = db.Column(db.Enum)
    market_cap = db.Column(db.Integer)
    name = db.Column(db.String(50))
    primary_exchange = db.Column(db.String(10))
    sic_code = db.Column(db.String(10))
    sic_description = db.Column(db.Text)
    total_employees = db.Column(db.Integer)
    type = db.Column(db.String(10))
    weighted_shares_outstanding = db.Column(db.Integer)
    
    def __repr__(self):
        return self.ticker
    
    users = db.relationship("User", secondary="userwatchlist", back_populates="watchlistentries")


db.Table(
    "userwatchlist",
    db.Column("user_id", db.ForeignKey("users.id"), primary_key=True),
    db.Column("tickerdetail_id", db.ForeignKey("tickerdetails.id"), primary_key=True)    
)

# db.Table(
#     "usertransactions",
#     db.Column("user_id", db.ForeignKey("users.id"), primary_key=True),
#     db.Column("transaction_id", db.ForeignKey("transactions.id"), primary_key=True)    
# )