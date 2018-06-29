import bufferred_rushare as ts
import sqlite3 as lite

from pandas.io import sql
import pandas as pd


# run_func_demo
from rqalpha.api import *
from rqalpha import run_func

import numpy as np
import datetime


def log_cash(context):
    pass


def init(context):
    de = all_instruments('CS')
    current = np.datetime64(datetime.datetime.now())   
    for indexs in de.index:
        #print(de.loc[indexs])
        order_book_id = de.loc[indexs].order_book_id
        listed_date = de.loc[indexs].listed_date
        order_book_id = order_book_id.split(".")
        order_book_id = order_book_id[0]

        listed_date = first_date = current
        last_date=first_date-np.timedelta64(5, 'D')
        listed_date = np.datetime64(listed_date)
        while listed_date>last_date:
            listed_date-=np.timedelta64(1, 'D')
            listed_date_str =  listed_date.astype(object) 

            listed_date_str = datetime.datetime.strftime(listed_date_str,"%Y-%m-%d") 
            #listed_date = listed_date._date_repr
            ts.get_tick_data(order_book_id,listed_date_str,retry_count=10,pause=10.0)
            print(order_book_id,listed_date_str)

    pass





def before_trading(context):
    pass


def handle_bar(context, bar_dict):
    pass



config = {
  "base": {
    "start_date": "2016-06-01",
    "end_date": "2016-12-01",
    "benchmark": "000300.XSHG",
    "accounts": {
        "stock": 100000
    }
  },
  "extra": {
    "log_level": "none",
  },
  "mod": {
    "sys_analyser": {
      "enabled": False,
      "plot": False
    }
  }
}

# 您可以指定您要传递的参数
run_func(init=init, before_trading=before_trading, handle_bar=handle_bar, config=config)








