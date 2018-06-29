
# -*- coding: utf-8 -*-

from rqalpha import run_code
from rqalpha import run_file
from rqalpha import run



code = """
from rqalpha.api import *


def init(context):
    logger.info("init")
    context.s1 = "000001.XSHE"
    update_universe(context.s1)
    context.fired = False
    print("context is:")
    print(context)



def before_trading(context):
    pass


def handle_bar(context, bar_dict):
    if not context.fired:
        # order_percent并且传入1代表买入该股票并且使其占有投资组合的100%
        order_percent(context.s1, 1)
        context.fired = True
"""

config1 = {
    "base": {
        "securities": "future",
        "start_date": "2015-01-09",
        "end_date": "2015-03-09",
        "frequency": "1d",
        "matching_type": "current_bar",
        "future_starting_cash": 1000000,
        "benchmark": None,
    },
    "extra": {
        "log_level": "error",
    },
    "mod": {
        "sys_progress": {
            "enabled": True,
            "show": True,
        },
    },
}


config2 = {
  "base": {
    "start_date": "2016-06-01",
    "end_date": "2016-12-01",
    "benchmark": "000300.XSHG",
    "accounts": {
      "stock": 100000,
    }
  },
  "extra": {
    "log_level": "error",
  },
  "mod": {
    "sys_analyser": {
      "enabled": True,
      "plot": True
    }
  }
}


strategy_file_path = "./buy_and_hold.py"
strategy_file_path = "./rsi.py"
strategy_file_path = "./macd.py"
strategy_file_path = "./IF_macd.py"
strategy_file_path = "./golden_cross.py"
strategy_file_path = "./turtle.py"

#run_code(code, config2)
#run(strategy_file_path)

run_file(strategy_file_path, config2)

