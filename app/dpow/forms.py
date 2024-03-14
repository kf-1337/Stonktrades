from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms_alchemy import QuerySelectMultipleField
from wtforms import widgets, SelectField
from ..models import Tickerdetail

# def watchlist_query():
#     return UserWatchlist.query.filter(UserWatchlist.username == current_user.username, UserWatchlist.ticker == ticker)

class QuerySelectMultipleFieldWithCheckboxes(QuerySelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class WatchlistForm(FlaskForm):
    watchlist = QuerySelectMultipleFieldWithCheckboxes("Watchlist")
    # watchlist = BooleanField('Watchlist')
    # submit = SubmitField('Change preference')

class BuyForm(FlaskForm):
    amount = IntegerField('Amount you want to buy: ', validators=[DataRequired(), Length(min=1, max=5)])
    submit = SubmitField('BUY')

class SellForm(FlaskForm):
    amount = IntegerField('Amount you want to sell: ', validators=[DataRequired(), Length(min=1, max=5)])
    submit = SubmitField('SELL')