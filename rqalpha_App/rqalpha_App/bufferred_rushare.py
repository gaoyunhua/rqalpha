
import sqlite3 as lite
from pandas.io import sql
from datetime import date

import pandas as pd


import six
import tushare as ts
from datetime import date
from dateutil.relativedelta import relativedelta
from rqalpha.data.base_data_source import BaseDataSource



cnx = None
cnxname=None

#def save_data(df,code=None, date=None,table="tickdata"):
#    start_conn(code)
#    sadasd=12312
    #sql.write_frame(df, name=table, con=cnx)
    #sql.read_sql(sql, name=table, con=cnx,if_exists="replace",index=True)
    #df.set_index("time")
    #sql.to_sql(df, name=table, con=cnx,if_exists="append",index=True)
    #sql.write_frame(df, name=table, con=cnx)
    #sql_df=df.loc[:,['volume','type','time','price']]

    #將 sql_df 資料寫入 Table名稱 Daily_Record 內

    #if_exists 預設為 failed 新建一個 Daily_Record table 並寫入 sql_df資料
    #sql.write_frame(sql_df, name=table, con=cnx)

    #if_exists 選擇 replace 是Daily_Record 這個 table 已存在資料庫
    #將Daily_Record 表刪除並重新創建 寫入 sql_df 的資料
    #sql.write_frame(sql_df, name=table, con=cnx, if_exists='replace')
    #if_exists 選擇 appnd 是 Daily_Record 這個 table 已存在資料庫 將 sql_df 的資料 Insert 進去
    #sql.write_frame(sql_df, name=table, con=cnx, if_exists='append')
def get_tick_data_local(code=None, date=None, retry_count=3, pause=0.001,src='sn'):
    start_conn(code)

    #選取dataframe 要寫入的欄位名稱
    #欄位名稱需與資料庫的欄位名稱一樣 才有辦法對照寫入
    table_name_str = date.replace('-','_')
    table_name_str = "d%s" % table_name_str

    if sql.has_table(table_name=table_name_str,con=cnx):
        sqlstr = 'select * from %s' % (table_name_str)
        df = sql.read_sql(sqlstr, con=cnx)
        return df

    #df = cnx.get_table(table_name=date)
#    df = cnx.read_query(sqlstr)
    #df = pd.read_sql(sql=sqlstr, con=cnx)

    #df = pd.read_sql_table(table_name=date,cnx)
    

def save_tick_data_local(df,code=None, date=None,table="tickdata"):
    start_conn(code)
    #cnx = lite.connect(code)
    #sql.write_frame(df, name=date, con=cnx)
    table_name_str = date.replace('-','_')
    table_name_str = "d%s" % table_name_str
    cnxsql = sql.pandasSQL_builder(cnx)
    cnxsql.to_sql(df, name=table_name_str, if_exists='replace')
    return df

def start_conn(name):
    global cnx
    global cnxname
    if cnx is None:
        cname="tickdata\%s"%name
        cnx = lite.connect(cname)
        #cnx = sql.pandasSQL_builder(cnx)
        cnxname=name
    else:
        if cnxname!=name:
            cname="tickdata\%s"%name
            cnx = lite.connect(cname)
            cnxname=name
            #cnx = sql.pandasSQL_builder(cnx)


def save_tick_data(df,code=None, date=None,table="tickdata"):
    save_tick_data_local(df,code,date,"tickdata")

def get_tick_data(code=None, date=None, retry_count=3, pause=0.001,src='sn'):
    df = get_tick_data_local(code, date, retry_count, pause,src)
    if df is None:
        df = ts.get_tick_data(code, date, retry_count, pause,src)
        if df is not None:
                save_tick_data(df,code, date)
    return df
        







class TushareKDataSource(BaseDataSource):
    @staticmethod
    def get_tushare_k_data(instrument, start_dt, end_dt):

        # 首先获取 order_book_id 并将其转换为 tushare 所能识别的 code
        order_book_id = instrument.order_book_id
        code = order_book_id.split(".")[0]

        # tushare 行情数据目前仅支持股票和指数，并通过 index 参数进行区分
        if instrument.type == 'CS':
            index = False
        elif instrument.type == 'INDX':
            index = True
        else:
            return None

        # 调用 tushare 函数，注意 datetime 需要转为指定格式的 str
        return ts.get_k_data(code, index=index, start=start_dt.strftime('%Y-%m-%d'), end=end_dt.strftime('%Y-%m-%d'))

    def get_bar(self, instrument, dt, frequency):

        # tushare k线数据暂时只能支持日级别的回测，其他情况甩锅给默认数据源
        if frequency != '1d':
            return super(TushareKDataSource, self).get_bar(instrument, dt, frequency)

        # 调用上边写好的函数获取k线数据
        bar_data = self.get_tushare_k_data(instrument, dt, dt)

        # 遇到获取不到数据的情况，同样甩锅；若有返回值，注意转换格式。
        if bar_data is None or bar_data.empty:
            return super(TushareKDataSource, self).get_bar(instrument, dt, frequency)
        else:
            return bar_data.iloc[0].to_dict()

    def history_bars(self, instrument, bar_count, frequency, fields, dt, skip_suspended=True):
        # tushare 的k线数据未对停牌日期做补齐，所以遇到不跳过停牌日期的情况我们先甩锅。有兴趣的开发者欢迎提交代码补齐停牌日数据。
        if frequency != '1d' or not skip_suspended:
            return super(TushareKDataSource, self).history_bars(instrument, bar_count, frequency, fields, dt, skip_suspended)

        # 参数只提供了截止日期和天数，我们需要自己找到开始日期
        # 获取交易日列表，并拿到截止日期在列表中的索引，之后再算出开始日期的索引
        start_dt_loc = self.get_trading_calendar().get_loc(dt.replace(hour=0, minute=0, second=0, microsecond=0)) - bar_count + 1
        # 根据索引拿到开始日期
        start_dt = self.get_trading_calendar()[start_dt_loc]

        # 调用上边写好的函数获取k线数据
        bar_data = self.get_tushare_k_data(instrument, start_dt, dt)

        if bar_data is None or bar_data.empty:
            return super(TushareKDataSource, self).get_bar(instrument, dt, frequency)
        else:
            # 注意传入的 fields 参数可能会有不同的数据类型
            if isinstance(fields, six.string_types):
                fields = [fields]
            fields = [field for field in fields if field in bar_data.columns]

            # 这样转换格式会导致返回值的格式与默认 DataSource 中该方法的返回值格式略有不同。欢迎有兴趣的开发者提交代码进行修改。
            return bar_data[fields].as_matrix()



    def available_data_range(self, frequency):
        return date(2005, 1, 1), date.today() - relativedelta(days=1)

