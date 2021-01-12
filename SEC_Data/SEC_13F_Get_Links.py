###############################
#Get web links for 13F filings# 
###############################

#Import python packages
import bs4
import requests
import pandas as pd

#Read in 13F root links data
df_13F = pd.read_csv('C:/Users/12407/Desktop/Education/Projects/SEC/df13F.csv')
data_13F = df_13F[:10]
data_13F['Url'] = ''

#Get 13 web links
for ind in data_13F.index: 
    res = requests.get(data_13F['Link'][ind])
    res.raise_for_status()
    bs4Soup = bs4.BeautifulSoup(res.text, 'html.parser')
    url = (bs4Soup.find_all("table", {"summary": "Directory Listing for $full_dir"})[0]
        .find_all('tr')[4].find_all('a', href=True)[0]['href'])
    data_13F['Url'][ind] = 'https://www.sec.gov' + url

