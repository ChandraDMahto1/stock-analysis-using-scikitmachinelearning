# -*- coding: utf-8 -*-
"""
Created on Thu Apr 02 10:39:51 2015

@author: CHANDRA DEO MAHTO
"""

import pandas as pd
import os
from Quandl import Quandl
import time
auth_tok=open("test.txt","r").read()

#data=Quandl.get("WIKI/KO",trim_start="2000-12-12",trim_end="2014-12-30",authtok=auth_tok)
path="D:/intraQuarter/intraQuarter"
def Stock_Prices():
    df=pd.DataFrame()
    statspath = path+'/_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)]
    print (stock_list)
    for each_dir in stock_list[1:]:
            try:
                ticker = each_dir.split("\\")[1]
                print(ticker)
                name = "WIKI/"+ticker.upper()
                data = Quandl.get(name,
                                  trim_start = "2000-12-12",
                                  trim_end = "2014-12-30",
                                  authtoken=auth_tok)
                data[ticker.upper()] = data["Adj. Close"]
                df = pd.concat([df, data[ticker.upper()]], axis = 1)

            except Exception as e:
                print(str(e))
                time.sleep(10)

    
                
            try:
                ticker = each_dir.split("\\")[1]
                print(ticker)
                name = "WIKI/"+ticker.upper()
                data = Quandl.get(name,
                                  trim_start = "2000-12-12",
                                  trim_end = "2014-12-30",
                                  authtoken=auth_tok)
                data[ticker.upper()] = data["Adj. Close"]
                df = pd.concat([df, data[ticker.upper()]], axis = 1)

           except Exception as e:
                print(str(e))
     
            
    df.to_csv("stock_prices.csv")


Stock_Prices()