import bufferred_rushare as ts
import sqlite3 as lite

from pandas.io import sql
import pandas as pd
import numpy as np

import datetime
import time

import matplotlib.pyplot as plt      #python画图包

__all__ = ["GetDayData","DayData"]

def GetDayData(df,date=None):
    def datefstr(date_string):
        #dd = datetime.datetime.strptime(date_string, '%H:%M:%S')
        #dd = time.mktime(dd.timetuple())
        #

        date_string="1970-1-1" + " " + date_string
        #dd = time.mktime(time.strptime(date_string, "%Y-%m-%d %H:%M:%S"))  
        return time.mktime(time.strptime(date_string, "%Y-%m-%d %H:%M:%S"))  

    def NumbericType(type_string):
        #dd = datetime.datetime.strptime(date_string, '%H:%M:%S')
        #dd = time.mktime(dd.timetuple())
        #

        if type_string=="买盘" :
            return 1
        if type_string=="卖盘" :
            return -1
        return 0

    def NumbericChange(change_string):
        #dd = datetime.datetime.strptime(date_string, '%H:%M:%S')
        #dd = time.mktime(dd.timetuple())
        #
        try:
            return float(change_string)
        except ValueError:
            return 0



#    df["rprice"] = df["price"].astype(np.float)
    df["rtime"] = df["time"].apply(datefstr)
    #df["rchange"] = df["change"].astype(np.float)
    #df["rchange"] = df["change"].astype('category')
    df["rchange"] = df["change"].apply(NumbericChange)
#    df["rvolume"] = df["volume"].astype(np.int)
    #df["rtype"] = df["type"].astype('category')
    df["rtype"] = df["type"].apply(NumbericType)
#    df["ramount"] = df["amount"].astype(np.int)

    return df


class DayData():
    def __init__(self,df):
        self.data = df
    def get_day_parameter(self):
        price = self.data["price"]
        datax = {
            'max':price.max(),
            'min':price.min(),
            'avg':price.mean(),
            'mid':price.median(),
            'start':price[0],
            'end':price[price.size-1],
            'std':price.std(),
            'skew':price.skew(),
            'sem':price.sem(),
            'mad':price.mad(),
            }
        #self.newdata = pd.DataFrame.from_dict(data=datax)
        self.newdata=pd.DataFrame.from_dict(datax,orient='index')
        #self.newdata = your_df_from_dict
        pass
    def set_code(self,code):
        self.newdata.code = code
    pass





from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances




def modelfix(Z):
    
    #del X['index']
    #del X['time']
    #del X['change']
    #del X['type']
    #del X['amount']
    X = Z["price"].to_frame()
    X["volume"] = Z["volume"]


    factor = (X["price"].max()-X["price"].min())/(X["volume"].max()-X["volume"].min())
    X['volume']*=factor

    n_clusters = 8
    model = AgglomerativeClustering(n_clusters=n_clusters,linkage="average")
    y_pred1 = model.fit(X)
    y_pred1 = y_pred1.labels_
    y_pred1 = y_pred1.astype(np.int32)

    #plt.figure(figsize=(12, 12))
    #plt.subplot(1, 2, 1)
    #plt.scatter(X["volume"], X["price"],c=y_pred1)


    model = KMeans(n_clusters=n_clusters)
    y_pred = model.fit_predict(X)


    #plt.subplot(1, 2, 2)
   # plt.scatter(X["volume"], X["price"],c=y_pred)
    #plt.show()

    return Z

def plotdata(Z):
    #plt.figure(figsize=(12, 12))
    #plt.subplot(111)  #在2图里添加子图1
    #plt.scatter(X["amount"], X["price"], c=y_pred) #scatter绘制散点
    #plt.title("Incorrect Number of Blobs")   #加标题

    from mpl_toolkits.mplot3d import Axes3D
    data = np.random.randint(0, 255, size=[40, 40, 40])

    x, y, z = data[0], data[1], data[2]
    ax = plt.subplot(111, projection='3d')  # 创建一个三维的绘图工程
    #  将数据点分成三部分画，在颜色上有区分度
    ax.scatter(Z["rtime"],Z["price"],Z["volume"], c=Z["rtype"]+3)  # 绘制数据点


    ax.set_zlabel('Z')  # 坐标轴
    ax.set_ylabel('Y')
    ax.set_xlabel('X')
    plt.show()


