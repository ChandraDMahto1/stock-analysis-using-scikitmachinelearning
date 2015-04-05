# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 23:32:53 2015

@author: CHANDRA DEO MAHTO
"""

import pandas as pd
import os
import time
from datetime import datetime


from time import mktime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
style.use("dark_background")
import re      #for regular expression

path="D:/intraQuarter/intraQuarter"
def Key_Stats(gather="Total Debt/Equity (mrq)"):
    statspath=path+'/_KeyStats'
    stock_list=[x[0] for x in os.walk(statspath)]  #contains list of subfolders(directories) under _keystats folder
    #print (stock_list)
    
    df=pd.DataFrame(columns=['Date',
                             'Unix',
                             'Ticker',
                             'DE Ratio',
                             'Price',
                             'stock_p_change',
                             'SP500',
                             'sp500_p_change',
                             'Difference',
                             'Status']) #creating the list for storing the structured data
    sp500_df=pd.DataFrame.from_csv("YAHOO-INDEX_GSPC.csv")    
    ticker_list=[]
    for each_dir in stock_list[1:25]:
        each_file=os.listdir(each_dir) #taking every file(html) from each directory
        #print (each_file)
        #time.sleep(15)
        ticker=each_dir.split("\\")[1]
        ticker_list.append(ticker)
        starting_stock_value=False
        starting_sp500_value=False
        
        
        
        if len(each_file)>0:
            for file in each_file:
                date_stamp=datetime.strptime(file,'%Y%m%d%H%M%S.html')
                unix_time=time.mktime(date_stamp.timetuple())
                #print (date_stamp,unix_time)
                full_file_path=each_dir + '/' + file  #gives path to our file                
                #print (full_file_path)
                source=open(full_file_path,'r').read()
                #print (source)
                try:
                    try:                    #for checking those values which cannot be converted to float
                        value=float(source.split(gather+':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0])
                    except Eception as e:
                        value=float(source.split(gather+':</td>\n<td class="yfnc_tabledata1">')[1].split('</td>')[0])  #as the data is constantly modified the source code also gats modified so they may can introduce a new line
                        #print(str(e),ticker,file)
                        #time.sleep(15)
                
                    try:
                         sp500_date=datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
                         row=sp500_df[(sp500_df.index==sp500_date)]
                         sp500_value=float(row["Adjusted Close"])
                    except:
                         sp500_date=datetime.fromtimestamp(unix_time-259200).strftime('%Y-%m-%d')
                         row=sp500_df[(sp500_df.index==sp500_date)]
                         sp500_value=float(row["Adjusted Close"])
                    try:                    
                       stock_price=float(source.split('</small><big><b>')[1].split('</b></big>')[0])
                    except Exception as e:
                        #<span id="yfs_110_afl">43..27</span>  #throws exception at this,to solve we use regular expression
                       try:                       
                           stock_price=(source.split('</small><big><b>')[1].split('</b></big>')[0])
                           stock_price=re.search(r'(\d(1,8)\.\d(1,8))',stock_price)  #wiil be searching for regular expressions with digits followed by atermination then again a digit (1,8) corresponds length
                           stock_price=float(stock_price.group(1))
                           print (stock_price)
                           time.sleep(15)
                           print (str(e),ticker,file)
                       except Exception as e:
                                        stock_price=(source.split('<span class="time_rtq_ticker">')[1].split('</span>')[0]) #added to avoid the error of real time ticker being added
                                        stock_price=re.search(r'(\d(1,8)\.\d(1,8))',stock_price)  #wiil be searching for regular expressions with digits followed by atermination then again a digit (1,8) corresponds length
                                        if stock_price:                                        
                                            stock_price=float(stock_price.group(1))
                                            print ('latest: ',stock_price)                                        
                                            
                                            print ('stock_price',str(e),ticker,file)
                                            time.sleep(15)
                    
                    #print("stock price:",stock_price,"ticker:",ticker)
                    
                    if not starting_stock_value:
                        starting_stock_value=stock_price
                    if not starting_sp500_value:
                        starting_sp500_value=sp500_value
                    
                    stock_p_change=((stock_price-starting_stock_value)/starting_stock_value)*100
                    sp500_p_change=((sp500_value-starting_sp500_value)/starting_sp500_value)*100
                    
                    difference=stock_p_change-sp500_p_change
                    if difference>0:
                        status="Outperform"
                    else:
                        status="Underperform"
                    
                    df=df.append({'Date':date_stamp,
                    'Unix':unix_time,
                    'Ticker':ticker,
                    'DE Ratio':value,
                    'Price':stock_price,
                    'stock_p_change':stock_p_change,
                    'SP500':sp500_value,
                    'sp500_p_change':sp500_p_change,
                    'Difference':difference,
                    'Status':status},ignore_index=True)
                except Exception as e:
                      pass                    
                    #print (str(e))
            for each_ticker in ticker_list:
                try:
                    plot_df=df[(df['Ticker']==each_ticker)]
                    plot_df=plot_df.set_index(['Date'])
                    if plot_df['Status'][-1]=="Underperform":
                        color='r'
                    else:
                        color='g'
                    
                    
                    
                    
                    plot_df['Difference'].plot(label=each_ticker,color=color)
                    plt.legend()
                except:
                    pass
                plt.show()
            save =gather.replace(' ','').replace(')','').replace('(','').replace('/','')+('.csv')
            #print (save)
            df.to_csv(save)
    


          # print (ticker + ":" ,value)                
            time.sleep(15)
Key_Stats()