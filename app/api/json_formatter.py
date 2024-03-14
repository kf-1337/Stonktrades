# this file contains the function to deliver data gotten from data_getter.py to the graphs using graph.js

from .data_getter import *

def print_labels_topx(raw_data_dict_topx:dict[str,float]):
   temp = '"' + '", "'.join(raw_data_dict_topx.keys()) + '"'
   print(temp)
   return temp

def print_values_topx(raw_data_dict_topx:dict[str,float]):
   printed_values_topx = []
   for x in raw_data_dict_topx.values():
      printed_values_topx.append("{:0.2f}".format(x))
   print(','.join(printed_values_topx))
   return ','.join(printed_values_topx)

def dashboard_topX(x):
   print('x=', x)
   # Getting Data from data_getter.py via function db_get_topx
   # return will be a dictionary with x+1 datasets
   # The +1 being the REST of the portfolio

   returned_data_topx = db_get_topx(x)

   return '''{
   "type":"pie",
   "data":{
      "labels":[%s],
      "datasets":[
         {
            "label":"Value of Stonk",
            "data":[%s],
            "borderWidth":1
         }
      ]
   },
   "options":{
      "layout":{
         "padding":10
      },
      "scales":{
         "y":{
            "beginAtZero":true
         }
      }
   }
}''' % (print_labels_topx(returned_data_topx), print_values_topx(returned_data_topx))


def print_labels_dash_over_time(raw_data_dict_dash_over_time:dict[str,float]):
   temp = '"' + '", "'.join(raw_data_dict_dash_over_time.keys()) + '"'
   print(temp)
   return temp

def print_values_dash_over_time(raw_data_dict_dash_over_time:dict[str,float]):
   printed_values_dash_over_time = []
   for y in raw_data_dict_dash_over_time.values():
      if int(y) >=0:
         printed_values_dash_over_time.append("{:0.2f}".format(int(y)))
      else:
         printed_values_dash_over_time.append(y)
   print(', '.join(printed_values_dash_over_time))
   return ', '.join(printed_values_dash_over_time)

def print_labels_stonk_chart(raw_data_dict_dash_over_time:dict[str,float]):
   temp = '"' + '", "'.join(raw_data_dict_dash_over_time.keys()) + '"'
   return temp

def print_values_stonk_chart(raw_data_dict_dash_over_time:dict[str,float]):
   printed_values_dash_over_time = []
   for y in raw_data_dict_dash_over_time.values():
      printed_values_dash_over_time.append("{:0.2f}".format(y))
   return ', '.join(printed_values_dash_over_time)


def dash_dash_over_time(y):
   print('y=', y)
   # Getting Data from data_getter.py via function db_get_topx
   # return will be a dictionary with x+1 datasets
   # The +1 being the REST of the portfolio
   returned_data_dash_over_time = db_get_dash_over_time(y)

   return '''{
   "type":"line",
   "data":{
      "labels":[%s],
      "datasets":[
         {
            "label": "Portfolio over time",
            "data":[%s],
            "borderColor": "rgb(0, 51, 204)",
            "borderWidth":1
         }
      ]
   },
   "options":{
      "layout":{
         "padding":10
      },
      "scales":{
         "y":{
            "beginAtZero":false
         }
      }
   }
}''' % (print_labels_dash_over_time(returned_data_dash_over_time), print_values_dash_over_time(returned_data_dash_over_time))


def json_format_stonk_chart(y, s):
   print('Trigger json_format_stonk_chart y=', y, "s=", s)
   # Getting Data from data_getter.py via function db_get_topx
   # return will be a dictionary with x+1 datasets
   # The +1 being the REST of the portfolio
   returned_db_get_stonk_chart = db_get_stonk_chart(y, s)

   return '''{
   "type":"line",
   "data":{
      "labels":[%s],
      "datasets":[
         {
            "label": "Stonk over time",
            "data":[%s],
            "borderColor": "rgb(0, 51, 204)",
            "borderWidth":1
         }
      ]
   },
   "options":{
      "layout":{
         "padding":10
      },
      "scales":{
         "y":{
            "beginAtZero":false
         }
      }
   }
}''' % (print_labels_stonk_chart(returned_db_get_stonk_chart), print_values_stonk_chart(returned_db_get_stonk_chart))
