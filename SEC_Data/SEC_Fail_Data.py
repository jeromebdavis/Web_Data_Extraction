##################################
#Create files with SEC fails data# 
##################################

#Import python packages
import bs4
import requests
import pandas as pd
import os
import wget
from zipfile import ZipFile 

#Set current working directory to fails data folder
print('Current Working Directory' , os.getcwd())
os.chdir('C:/Users/12407/Desktop/Education/Projects/SEC/Fail_Data')
print('New Working Directory' , os.getcwd())

#Get links for each fail data file
res = requests.get('https://www.sec.gov/data/foiadocsfailsdatahtm')
res.raise_for_status()
bs4Soup = bs4.BeautifulSoup(res.text, 'html.parser')
links = []
for link in bs4Soup.find_all("table")[1].find_all('a', href=True):
    links.append('https://www.sec.gov' + link.get('href'))

#Download and extract fails data to fails data folder 
for link in links:
    filename = wget.download(link)
    link = link.replace('https://www.sec.gov/files/data/fails-deliver-data/','')
    link = link.replace('https://www.sec.gov/files/data/frequently-requested-foia-document-fails-deliver-data/','')
    ZipFile(link, 'r').extractall()

#Create list of extracted fails data text files
files = []
for file in os.listdir("C:/Users/12407/Desktop/Education/Projects/SEC/Fail_Data"):
    if file.endswith(".txt"):
        files.append(file)

#files = ['cnsfail201305a.txt', 'cnsfail201305b.txt']

#Get CUSIP Ticker Lookup table
df_fails = pd.DataFrame(columns=[1,2])
for file in files:
    infile = open(file, "r").read().replace('YUM| BRANDS','YUM BRANDS').splitlines()
    lines = infile[1:len(infile)-2]
    records = [tuple(line.split('|')) for line in lines]
    df = pd.DataFrame(records)
    df = df.drop([0,3,4,5], axis=1)
    df_fails = df_fails.append(df)
    df_fails = df_fails.drop_duplicates(subset=[1,2])
    print(file)
df_fails.columns = ['CUSIP','Ticker','XXX']
df_fails = df_fails.drop(['XXX'], axis=1)
df_fails = df_fails.sort_values(by=['CUSIP','Ticker'])
df_fails.to_csv('C:/Users/12407/Desktop/Education/Projects/SEC/CUSIP_Ticker.csv',index=False)

#Collect all SPY company data files and export
df_fails = pd.DataFrame(columns=[0,1,2,5])
for file in files:
    infile = open(file, "r").read().replace('YUM| BRANDS','YUM BRANDS').splitlines()
    lines = infile[1:len(infile)-2]
    records = [tuple(line.split('|')) for line in lines]
    df = pd.DataFrame(records)
    df = df.drop([3,4], axis=1)
    df1 = df[df[2].isin(['A','AAL','AAP','AAPL','ABBV','ABC','ABMD','ABT','ACN','ADBE',
             'ADI','ADM','ADP','ADS','ADSK','AEE','AEP','AES','AFL','AGN','AIG','AIV',
             'AIZ','AJG','AKAM','ALB','ALGN','ALK','ALL','ALLE','ALXN','AMAT','AMCR',
             'AMD','AME','AMG','AMGN','AMP','AMT','AMZN','ANET','ANSS','ANTM','AON',
             'AOS','APA','APD','APH','APTV','ARE','ARNC','ATO','ATVI','AVB','AVGO',
             'AVY','AWK','AXP','AZO','BA','BAC','BAX','BBT','BBY','BDX','BEN','BF.B',
             'BHGE','BIIB','BK','BKNG','BLK','BLL','BMY','BR','BRK.B','BSX','BWA',
             'BXP','C','CAG','CAH','CAT','CB','CBOE','CBRE','CBS','CCI','CCL','CDNS',
             'CE','CELG','CERN','CF','CFG','CHD','CHRW','CHTR','CI','CINF','CL','CLX',
             'CMA','CMCSA','CME','CMG','CMI','CMS','CNC','CNP','COF','COG','COO','COP',
             'COST','COTY','CPB','CPRI','CPRT','CRM','CSCO','CSX','CTAS','CTL','CTSH',
             'CTVA','CTXS','CVS','CVX','CXO','D','DAL','DD','DE','DFS','DG','DGX','DHI'])]
    df2 = df[df[2].isin(['DHR','DIS','DISCA','DISCK','DISH','DLR','DLTR','DOV','DOW',
             'DRE','DRI','DTE','DUK','DVA','DVN','DXC','EA','EBAY','ECL','ED','EFX',
             'EIX','EL','EMN','EMR','EOG','EQIX','EQR','ES','ESS','ETFC','ETN','ETR',
             'EVRG','EW','EXC','EXPD','EXPE','EXR','F','FANG','FAST','FB','FBHS','FCX',
             'FDX','FE','FFIV','FIS','FISV','FITB','FLIR','FLS','FLT','FMC','FOX',
             'FOXA','FRC','FRT','FTI','FTNT','FTV','GD','GE','GILD','GIS','GL','GLW',
             'GM','GOOG','GOOGL','GPC','GPN','GPS','GRMN','GS','GWW','HAL','HAS',
             'HBAN','HBI','HCA','HCP','HD','HES','HFC','HIG','HII','HLT','HOG','HOLX',
             'HON','HP','HPE','HPQ','HRB','HRL','HSIC','HST','HSY','HUM','IBM','ICE',
             'IDXX','IEX','IFF','ILMN','INCY','INFO','INTC','INTU','IP','IPG','IPGP',
             'IQV','IR','IRM','ISRG','IT','ITW','IVZ','JBHT','JCI','JEC','JEF','JKHY',
             'JNJ','JNPR','JPM','JWN','K','KEY','KEYS','KHC','KIM','KLAC','KMB','KMI'])]
    df3 = df[df[2].isin(['KMX','KO','KR','KSS','KSU','L','LB','LDOS','LEG','LEN','LH',
             'LHX','LIN','LKQ','LLY','LMT','LNC','LNT','LOW','LRCX','LUV','LW','LYB',
             'M','MA','MAA','MAC','MAR','MAS','MCD','MCHP','MCK','MCO','MDLZ','MDT',
             'MET','MGM','MHK','MKC','MKTX','MLM','MMC','MMM','MNST','MO','MOS','MPC',
             'MRK','MRO','MS','MSCI','MSFT','MSI','MTB','MTD','MU','MXIM','MYL','NBL',
             'NCLH','NDAQ','NEE','NEM','NFLX','NI','NKE','NKTR','NLSN','NOC','NOV',
             'NRG','NSC','NTAP','NTRS','NUE','NVDA','NWL','NWS','NWSA','O','OKE',
             'OMC','ORCL','ORLY','OXY','PAYX','PBCT','PCAR','PEG','PEP','PFE','PFG',
             'PG','PGR','PH','PHM','PKG','PKI','PLD','PM','PNC','PNR','PNW','PPG',
             'PPL','PRGO','PRU','PSA','PSX','PVH','PWR','PXD','PYPL','QCOM','QRVO',
             'RCL','RE','REG','REGN','RF','RHI','RJF','RL','RMD','ROK','ROL','ROP',
             'ROST','RSG','RTN','SBAC','SBUX','SCHW','SEE','SHW','SIVB','SJM','SLB',
             'SLG','SNA','SNPS','SO','SPG','SPGI','SRE','STI','STT','STX','STZ','SWK',
             'SWKS','SYF','SYK','SYMC','SYY','T','TAP','TDG','TEL','TFX','TGT','TIF',
             'TJX','TMO','TMUS','TPR','TRIP','TROW','TRV','TSCO','TSN','TSS','TTWO',
             'TWTR','TXN','TXT','UA','UAA','UAL','UDR','UHS','ULTA','UNH','UNM','UNP',
             'UPS','URI','USB','UTX','V','VAR','VFC','VIAB','VLO','VMC','VNO','VRSK',
             'VRSN','VRTX','VTR','VZ','WAB','WAT','WBA','WCG','WDC','WEC','WELL','WFC',
             'WHR','WLTW','WM','WMB','WMT','WRK','WU','WY','WYNN','XEC','XEL','XLNX',
             'XOM','XRAY','XRX','XYL','YUM','ZBH','ZION','ZTS'])]    
    df = df1.append(df2).append(df3)
    df_fails = df_fails.append(df)
    print(file)
df_fails.columns = ['SDate','CUSIP','Symbol','Price','XXX']
df_fails = df_fails.drop(['XXX'], axis=1)
df_fails = df_fails.sort_values(by=['Symbol', 'SDate'])
df_fails.to_csv('C:/Users/12407/Desktop/Education/Projects/SEC/dffailsSPY.csv',index=False)

#split data by ticker first letter to increase  


#Collect all fails data files and export
#df_fails = pd.DataFrame(columns=[0,2,5])
#for file in files:
#    infile = open(file, "r").read().splitlines()
#    lines = infile[1:len(infile)-2]
#    records = [tuple(line.split('|')) for line in lines]
#    df = pd.DataFrame(records)
#    df = df.drop([1,3,4], axis=1)
#    df_fails = df_fails.append(df)
#    print(file)
#df_fails.columns = ['SDate','Symbol','Price']
#df_fails.to_csv('C:/Users/12407/Desktop/Education/Projects/SEC/dffails.csv',index=False)
