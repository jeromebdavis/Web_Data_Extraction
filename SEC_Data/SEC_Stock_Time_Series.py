##################################
#Create time series from SEC data# 
##################################

#Import python packages
import pandas as pd
import os
import re

#Set current working directory to fails data folder
print('Current Working Directory' , os.getcwd())
os.chdir('C:/Users/12407/Desktop/Education/Projects/SEC/Fail_Data')
print('New Working Directory' , os.getcwd())

#Create date data
years = ['2001','2002','2003','2004','2005','2006','2007','2008','2009','2010',
         '2011','2012','2013','2014','2015','2016','2017','2018','2019','2020']
months = ['01','02','03','04','05','06','07','08','09','10','11','12']
days_31 = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16',
          '17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
days_30 = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16',
          '17','18','19','20','21','22','23','24','25','26','27','28','29','30']
days_29 = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16',
          '17','18','19','20','21','22','23','24','25','26','27','28','29']
days_28 = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16',
          '17','18','19','20','21','22','23','24','25','26','27','28']
dates = []
for year in years:
    for month in months:
        if month in ['01','03','05','07','08','10','12']:        
            for day in days_31:
                dates.append(year+month+day)                        
        elif month in ['04','06','09','11']:
            for day in days_30:
                dates.append(year+month+day)                                    
        elif year in ['1992','1996','2000','2004','2008','2012','2016','2020']:
            for day in days_29:
                dates.append(year+month+day)                                                
        else:
            for day in days_28:
                dates.append(year+month+day)                                                
df_dates = pd.DataFrame(dates)
df_dates.columns = ['SDate']
df_dates['SDate'] = df_dates['SDate'].astype(str)
df_dates.to_csv('C:/Users/12407/Desktop/Education/Projects/SEC/df_dates.csv',index=False)

#Read in SEC fails data
df_symbols = pd.read_csv('C:/Users/12407/Desktop/Education/Projects/SEC/dffailsSPY.csv')
df_symbols = df_symbols[df_symbols['Price']!='.']
df_symbols['Price'] = df_symbols['Price'].astype(float)
df_symbols['SDate'] = df_symbols['SDate'].astype(str)

#Create blank dataframe for appending
df_data = pd.DataFrame(columns=['SDate','CUSIP','Symbol','Price'])

#Get ticker list from dataset
ticker_list = df_symbols['Symbol'].unique().tolist()

#For each ticker in ticker list
for ticker in ticker_list:

    df_symbol = df_symbols[df_symbols['Symbol']==ticker]    

    #Merge date and SEC fails data
    df_merged = pd.merge(df_dates, df_symbol, on='SDate', how='left')
    
    #Price values are listed as closing price on previous day. Need to shift date forward
    df_merged['SDate'] = df_merged['SDate'].shift(1)
    
    #Interpolate and fill in data between observations
    df_merged['Price'] = df_merged['Price'].interpolate(limit_area='inside')
    df_merged['Symbol'] = df_merged['Symbol'].fillna(method='bfill').fillna(method='ffill')
    df_merged['CUSIP'] = df_merged['CUSIP'].fillna(method='bfill').fillna(method='ffill')
    
    #Only include certain dates
    df_merged = df_merged[df_merged['SDate'].str[-4:].isin(['1231','0215',
                            '0331','0515','0630','0815','0930','1115'])]
    
    #Append data set to main df data data set
    df_data = df_data.append(df_merged)
    print(ticker)

df_data.to_csv('C:/Users/12407/Desktop/Education/Projects/SEC/dffailsSPYtime_series.csv',index=False)


