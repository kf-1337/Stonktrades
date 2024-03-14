from flask import request
from flask_login import login_required, current_user
from . import api
from .data_formatter import *
from .json_formatter import *

@api.route('/api/get_topx_data/')
def api_topx():
    x = request.args.get('x', default = 2, type = int)
    return dashboard_topX(x)

@api.route('/api/get_dash_over_time_data/')
def api_dash_over_time():
    y = request.args.get('y', default = "1m", type = str)
    return dash_dash_over_time(y)


@api.route('/api/get_stonks_chart_data/')
def api_stonks_chart():
    y = request.args.get('y', type = str)
    s = request.args.get('s', type = str)
    print("API Route: ",y, s)
    # print(json_format_stonk_chart(y))
    return json_format_stonk_chart(y, s)