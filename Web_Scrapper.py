import json
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

stock_symbol='KUANTUM.NS'

stock_url='https://in.finance.yahoo.com/quote/'+stock_symbol
url = stock_url
response = requests.get(url, timeout=240)
soup = BeautifulSoup(response.content, "html.parser")
price=soup.find_all('div', class_='My(6px) Pos(r) smartphone_Mt(6px)')[0].find('span').text

def get_children(html_content):
    return [item for item in html_content.children if len(str(item).replace("\n","").strip())>0]
    
def remove_multiple_spaces(string):
    if type(string)==str:
        return ' '.join(string.split())
    return string
    
def get_table_simple(table,is_table_tag=True):
    elems = table.find_all('tr') if is_table_tag else get_children(table)
    table_data = list()
    for row in elems:
        row_data = list()
        row_elems = get_children(row)
        for elem in row_elems:
            text = elem.text.strip().replace("\n","")
            text = remove_multiple_spaces(text)
            if len(text)==0:
                continue
            row_data.append(text)
        table_data.append(row_data)
    return table_data
    
my_table=get_table_simple(soup.find_all('div', class_='D(ib) W(1/2) Bxz(bb) Pend(12px) Va(t) ie-7_D(i) smartphone_D(b) smartphone_W(100%) smartphone_Pend(0px) smartphone_BdY smartphone_Bdc($seperatorColor)')[0].find('table'))

temp_list=my_table[4][1].split('-')
l=temp_list[0].strip()
h=temp_list[1].strip()
o=my_table[1][1].strip()
v=my_table[7][1].strip()
p=price.strip()
lo=l.replace(',','')
hi=h.replace(',','')
op=o.replace(',','')
vo=v.replace(',','')
cl=p.replace(',','')
low=float(lo)
high=float(hi)
open=float(op)
volume=float(vo)
close=float(cl)

my_list={'Open':[open],'High':[high],'Low':[low],'Close':[close],'Volume':[volume]}
mydf=pd.DataFrame.from_dict(my_list)

