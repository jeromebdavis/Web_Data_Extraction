############################
#Scrape SEC for 13F filings# 
############################

#Import python packages
import requests
import bs4
import pandas as pd

company_website_list = {
        'BAUPOST GROUP LLC/MA' : 'https://www.sec.gov/Archives/edgar/data/1061768/000156761919016587/xslForm13F_X01/form13fInfoTable.xml',
        'Appaloosa LP' : 'https://www.sec.gov/Archives/edgar/data/1656456/000165645619000006/xslForm13F_X01/Form13FInfoTable.xml',
        'MILLER VALUE PARTNERS, LLC' : 'https://www.sec.gov/Archives/edgar/data/1135778/000108514619002304/xslForm13F_X01/form13fInfoTable.xml',
        'GARDNER RUSSO & GARDNER LLC' : 'https://www.sec.gov/Archives/edgar/data/860643/000086064319000004/xslForm13F_X01/form13fInfoTable.xml',
        'Pershing Square Capital Management, L.P.' : 'https://www.sec.gov/Archives/edgar/data/1336528/000117266119001860/xslForm13F_X01/infotable.xml'
                }
df_all = pd.DataFrame(columns=[0,1,2,3,4,5,6,7,8,9,10,11,12])

for company, website in company_website_list.items():
    res = requests.get(website)
    res.raise_for_status()
    bs4Soup = bs4.BeautifulSoup(res.text, 'html.parser')
    table_list = bs4Soup.find_all('table')
    key_table = table_list[len(table_list)-1]
    key_table.getText()
    tr_list = key_table.find_all('tr')
    data_collect_all = []
    for tag in key_table.find_all('tr'):
        data_collect_td = []
        for tag2 in tag.find_all('td'):        
            data_collect_td.append(tag2.getText())       
        data_collect_all.append(data_collect_td)
    df = pd.DataFrame(data_collect_all)[3:]        
    df[12] = company
    df_all = df_all.append(df)

df_all.columns = [
        'col_1_name_of_issuer', 'col_2_title_of_class', 'col_3_cusip', 'col_4_value',
        'col_5_sh_prn_amt', 'col_5_sh_prn', 'col_5_put_call', 'col_6_inv_discretion',
        'col_7_manager', 'col_8_vote_sole', 'col_8_vote_shared', 'col_8_vote_none', 'company'
        ]



