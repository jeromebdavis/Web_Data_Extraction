################################
#Get root links for 13F filings# 
################################

#Import python packages
import requests
import pandas as pd

#Set start and current year and current quarter and quarters
start_year = 1994
current_year = 2018
current_quarter = 4
years = list(range(start_year, current_year))
quarters = ['QTR1', 'QTR2', 'QTR3', 'QTR4']

#Get information for all companies, filter to only include 13F filers, and create root links
df_13F = pd.DataFrame(columns=[0,1,2,3,4,5,6])
history = [(y, q) for y in years for q in quarters]
for i in range(1, current_quarter + 1):
    history.append((current_year, 'QTR%d' % i))
for x in history:
    url = 'https://www.sec.gov/Archives/edgar/full-index/%d/%s/master.idx' % (x[0], x[1])   
    lines = requests.get(url).content.decode("utf-8", "ignore").splitlines()
    records = [tuple(line.split('|')) for line in lines[11:]]
    temp = pd.DataFrame(records) 
    temp = temp[temp[2]=='13F-HR']
    temp[5] = x[0]
    temp[6] = x[1]
    temp[4] = ('https://www.sec.gov/Archives/' 
      + temp[4].str.strip().str.replace('-','').str.replace('.txt',''))
    df_13F = df_13F.append(temp)
    print(url)
df_13F.columns = ['CIK', 'Name', 'Type', 'Date', 'Link', 'Year', 'Qtr']
df_13F.to_csv('C:/Users/12407/Desktop/Education/Projects/SEC/df13F.csv',index=False)
