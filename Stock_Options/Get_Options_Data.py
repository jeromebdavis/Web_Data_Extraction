from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import bs4
import pandas as pd
from datetime import datetime
from datetime import date
import time
import re
import numpy as np 

#Change current working directory
os.chdir('C:/Users/12407/Desktop/Education/Projects/Investing_Options')

#Set chrome driver specifications
DRIVER_PATH = './chromedriver'
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(chrome_options=chrome_options, 
                          executable_path=DRIVER_PATH)

#Change current working directory
os.chdir('C:/Users/12407/Desktop/Education/Projects/Investing_Options/Options_Data')

#Create dataframe to append elements 
df = pd.DataFrame(columns = ['Ticker', 'Type', 'Contract_Name', 'Last_Trade_Date', 
    'Strike', 'Last_Price', 'Bid', 'Ask', 'Change', 'Pct_Change','Volume',
    'Open_Interest', 'Implied_Volatility', 'Ticker_Price', 'Avg_Price', 
    'Likely_Price', 'Profit_Pct', 'Flag'])

#List of tickers to get - Currently set to tickers in SYLD etf
ticker_list = [

        ["AYI",	"AER",	"AFL",	"ALL",	"ALLY",	"AMCX",	"AMP",	"AAPL",	"ARW",	"AGO",	"BKR",	"BIIB",	"BCC",	"BC",	"BKE",	"CBT",	"CVX",	"CFG",	"COP",	"CPA",	"CMI",	"CVI",	"DDS",	"DFS",	"DISCA"],
        ["DISCK",	"DISH",	"UFS",	"DD",	"ETN",	"ESI",	"FHI",	"FL",	"FOX",	"GME",	"GM",	"GES",	"HAL",	"HP",	"HPE",	"HFC",	"HWM",	"HPQ",	"HUN",	"INTC",	"IP",	"JPM",	"JNPR",	"LNC",	"LPX"],
        ["B3SPXZ",	"LYB",	"MTB",	"MAN",	"VAC",	"MCK",	"MDP",	"MET",	"MSM",	"MUR",	"NWSA",	"NUS",	"NUE",	"NVT",	"OLN",	"PNC",	"QRTEA",	"RL",	"RBC",	"RS",	"RCII",	"SANM",	"SLB",	"SWM",	"SLM"],
        ["SNA",	"STLD",	"STLA",	"SYF",	"TOL",	"TPH",	"TSE",	"TSN",	"UAL",	"UHS",	"UNM",	"USB",	"VLO",	"VIAC",	"VSH",	"VOYA",	"WDR",	"WBA",	"WFC",	"WU",	"WHR",	"INT",	"WOR",	"WYND",	"XRX"]
    
#        ["BHP",	"BBL",	"LIN",	"RIO",	"VALE",	"SHW",	"APD",	"ECL",	"DD",	"SCCO",	"NEM",	"GOLD",	"FCX",	"DOW",	"CRH",	"PPG",	"CTVA",	"LYB",	"NTR",	"MT",	"FNV",	"VMC",	"WPM",	"MLM",	"PKX",	"ALB",	"AEM",	"AVTR",	"SUZ",	"NUE"],
#        ["CE",	"FMC",	"SQM",	"EMN",	"JHX",	"SMG",	"IFF",	"SBSW",	"RPM",	"KL",	"MOS",	"TECK",	"WLK",	"AU",	"KGC",	"CF",	"CX",	"VEDL",	"GFI",	"SID",	"ACH",	"RS",	"CLF",	"STLD",	"RGLD",	"PAAS",	"GGB",	"ICL",	"AXTA",	"HUN"],
#        ["MDU",	"BTG",	"TX",	"MP",	"ASH",	"KWR",	"EXP",	"AUY",	"CC",	"NEU",	"ESI",	"WDFC",	"AG",	"X",	"SSRM",	"GRA",	"OLN",	"BAK",	"DNMR",	"AVNT",	"OSB",	"BCPC",	"AA",	"UFPI",	"AGI",	"UNVR",	"NG",	"HL",	"SXT",	"NGVT"],
#        ["LTHM",	"HMY",	"FUL",	"BVN",	"MEOH",	"SCL",	"CBT",	"CMC",	"LAC",	"AMRS",	"SUM",	"EQX",	"TRQ",	"CDE",	"TROX",	"IOSP",	"ITRO",	"MTX",	"PVG",	"EVA",	"CMP",	"EGO",	"TSE",	"SIM",	"PQG",	"MAG",	"BCC",	"OR",	"GCP",	"CSTM"],
#        ["UFS",	"KRO",	"IAG",	"GEVO",	"ABML",	"HBM",	"SA",	"FSM",	"MTRN",	"KALU",	"NGD",	"SILV",	"SAND",	"HCC",	"SWM",	"NEXA",	"FOE",	"SVM",	"LOMA",	"NINK",	"ORLA",	"CCF",	"OEC",	"DRD",	"KRA",	"CENX",	"NP",	"WLKP",	"SCHN",	"GATO"],
#        ["EXK",	"MERC",	"USCR",	"MMX",	"KOP",	"GLT",	"CPAC",	"GPRE",	"PLL",	"USLM",	"RFP",	"CLW",	"ASIX",	"HWKN",	"FF",	"LBTI",	"SMTS",	"AVD",	"MTL",	"MUX",	"TG",	"VHI",	"LOOP",	"RYAM",	"MTA",	"VNTR",	"GSS",	"HYMC",	"SXC",	"VRS"],
#        ["AXU",	"PLM",	"TGB",	"MSB",	"USAS",	"NAK",	"IPI",	"GSM",	"TMQ",	"GPL",	"BIOX",	"EMX",	"MBII",	"PLG",	"GLDG",	"ODC",	"GAU",	"THM",	"CINR",	"TMST",	"GSV",	"MCEM",	"GORO",	"RBTK",	"CMCL",	"ITRG",	"UAN",	"LWLG",	"FURY",	"TRX"],
#        ["TREC",	"WRN",	"ZEUS",	"MKD",	"KBLB",	"AUMN",	"METC",	"WWR",	"NTIC",	"SPPP",	"RRIF",	"CTGO",	"TMRC",	"ASM",	"VGZ"]

    ]

#Date of interest
Date_Interest = datetime(2021, 2, 19)

#Get integer value of date of interest
def unix_time(dt):
    return int((dt - datetime.utcfromtimestamp(0)).total_seconds())
date_integer = unix_time(Date_Interest)

#Loop through ticker_list 2d
for TickerL in ticker_list: 

    #Print sub ticker list
    print(TickerL)    

    #Loop through ticker list 2d
    for Ticker in TickerL:
    
        #Print current ticker
        print(Ticker)    
    
        try:
    
            #Create dataframe to append elements 
            df = pd.DataFrame(columns = ['Ticker', 'Type', 'Contract_Name', 'Last_Trade_Date', 
                                         'Strike', 'Last_Price', 'Bid', 'Ask', 'Change', 'Pct_Change','Volume',
                                         'Open_Interest', 'Implied_Volatility', 'Ticker_Price', 'Avg_Price', 
                                         'Likely_Price', 'Profit_Pct', 'Flag'])
            
            #Query data from url and parse it
            driver.get('https://finance.yahoo.com/quote/'+Ticker+'/options?p='+Ticker+'&date='+str(date_integer))
            time.sleep(5)
            res = driver.page_source
            bs4Soup = bs4.BeautifulSoup(res, 'html.parser')
            
            #Get ticker price
            Ticker_Price_Text = res.replace('"','').replace('(','').replace(')','')
            Ticker_Price = (re.findall('D\(ib\)" data-reactid="50">.+</span><span class="Trsdu', res)[0].
                            replace('D(ib)" data-reactid="50">','').replace('</span><span class="Trsdu',''))
            
            #Get option data
            data_list = []
            data_tags = bs4Soup.find_all('tr')
            for tag in data_tags:
                temp_list = []
                if data_tags.index(tag) == 0:
                    temp_tag = tag.select("th")            
                else:
                    temp_tag = tag.select("td")
                for tag_2 in temp_tag:
                    temp_list.append(tag_2.getText().strip())
                data_list.append(temp_list)
            
            #Put option data into two lists for calls and puts
            result = [[]]
            for i in data_list[1:]:
                if not i:
                    result.append([])
                else:
                    result[-1].append(i)
            
            #Process and perform calculations on call option data
            df_call = pd.DataFrame(result[0], columns = ['Contract_Name', 'Last_Trade_Date', 
                'Strike', 'Last_Price', 'Bid', 'Ask', 'Change', 'Pct_Change','Volume',
                'Open_Interest', 'Implied_Volatility'])
            #Bring in ticker price, ticker and type
            df_call['Ticker'] = Ticker
            df_call['Ticker_Price'] = Ticker_Price
            df_call['Type'] = 'Call'
            #Convert numeric columns to numeric type
            df_call[['Bid','Ask','Strike','Last_Price','Ticker_Price']] = (
                df_call[['Bid','Ask','Strike','Last_Price','Ticker_Price']].apply(pd.to_numeric))
            #Calculate average spread price
            df_call['Avg_Price'] = df_call[['Bid','Ask']].mean(axis=1)
            #Calculate most likely price to get which is minimum of average spread price and most recent price
            df_call['Likely_Price'] = df_call[['Avg_Price','Last_Price']].min(axis=1)
            #Calculate profit percentage
            df_call['Profit_Pct'] = df_call['Likely_Price']/df_call['Ticker_Price']
            #Add flag for strike price just above ticker price
            df_call['Flag_1'] = np.where(df_call['Ticker_Price']<df_call['Strike'], 'yes', 'no')
            df_call['Flag_2'] = df_call['Flag_1'].shift(1)
            df_call['Flag'] = np.where((df_call['Flag_1']=='yes') & (df_call['Flag_2']=='no'), 'yes', 'no')
            df_call = df_call.drop(['Flag_1','Flag_2'], axis=1)
            df = df.append(df_call)
            
            #Process and perform calculations on put option data
            df_put = pd.DataFrame(result[1], columns = ['Contract_Name', 'Last_Trade_Date', 
                'Strike', 'Last_Price', 'Bid', 'Ask', 'Change', 'Pct_Change','Volume',
                'Open_Interest', 'Implied_Volatility'])
            #Bring in ticker price, ticker and type
            df_put['Ticker'] = Ticker
            df_put['Ticker_Price'] = Ticker_Price
            df_put['Type'] = 'Put'
            #Convert numeric columns to numeric type
            df_put[['Bid','Ask','Strike','Last_Price','Ticker_Price']] = (
                df_put[['Bid','Ask','Strike','Last_Price','Ticker_Price']].apply(pd.to_numeric))
            #Calculate average spread price
            df_put['Avg_Price'] = df_put[['Bid','Ask']].mean(axis=1)
            #Calculate most likely price to get which is minimum of average spread price and most recent price
            df_put['Likely_Price'] = df_put[['Avg_Price','Last_Price']].min(axis=1)
            #Calculate profit percentage
            df_put['Profit_Pct'] = df_put['Likely_Price']/df_put['Strike']
            #Add flag for strike price just above ticker price
            df_put['Flag_1'] = np.where(df_put['Ticker_Price']<df_put['Strike'], 'yes', 'no')
            df_put['Flag_2'] = df_put['Flag_1'].shift(-1)
            df_put['Flag'] = np.where((df_put['Flag_1']=='no') & (df_put['Flag_2']=='yes'), 'yes', 'no')
            df_put = df_put.drop(['Flag_1','Flag_2'], axis=1)
            df = df.append(df_put)
    
            #Export dataframes to excel with Ticker 
            df.to_csv('Options_Data_'+Ticker+'.csv', index=False)
    
        except:
            
            print('error occured for ticker ' + Ticker)
            
            time.sleep(5)

    #Put extra time as yahoo only takes around 30 scrapes at a time
    time.sleep(150)        
        
#Create dataframe to append elements 
df = pd.DataFrame(columns = ['Ticker', 'Type', 'Contract_Name', 'Last_Trade_Date', 
    'Strike', 'Last_Price', 'Bid', 'Ask', 'Change', 'Pct_Change','Volume',
    'Open_Interest', 'Implied_Volatility', 'Ticker_Price', 'Avg_Price', 
    'Likely_Price', 'Profit_Pct', 'Flag'])

#Loop through tickers, append and export to csv with today's date 
current_date = datetime.today().strftime('%Y-%m-%d')
for TickerL in ticker_list: 
    for Ticker in TickerL:
        try:
            df_in = pd.read_csv('Options_Data_'+Ticker+'.csv')  
            df = df.append(df_in)
            print('Appended data for: ' + Ticker)
        except:
            print('No data for: ' + Ticker)
        
df.to_csv('Options_Data_'+current_date+'.csv', index=False)


