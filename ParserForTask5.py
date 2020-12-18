import lxml.html
import requests
from bs4 import BeautifulSoup
import csv
import os
import re
import pandas as pd

URL = 'http://notelections.online/region/region/st-petersburg?action=show&root=1&tvd=27820001217417&vrn=27820001217413&region=78&global=&sub_region=78&prver=0&pronetvd=null&vibid=27820001217417&type=222'
HOST = 'http://notelections.online'

def get_html(url):
    r = requests.get(url)
    return r

html = get_html(URL)
soup = BeautifulSoup(html.text, 'html.parser')
links_in_html = soup.find_all('a', href=True)
good_links = []

for link in links_in_html:
    if link['href'].startswith('/region/region/st-petersburg') and link['href'].endswith('222'):
        good_links.append(HOST + link['href'])
del(links_in_html)

def parse(html,n_tik):    
    def extract_values(row):
        values = []
        row_values = row.find_all('td')
        for row_value in row_values:
            values.append(int(re.findall(r'\d+',row_value.text)[0]))
        return values
    
    soup = BeautifulSoup(html.text, 'html.parser')
    table = soup.find_all('table')[-1]
    rows = table.find_all('tr')
    clear_rows = []
    for i,row in enumerate(rows):
        if i == 12:
            continue
        clear_rows.append(extract_values(row))
    data_tik = pd.DataFrame(data=clear_rows).transpose()
    data_tik['tik'] = [n_tik + 1 for _ in range (len(clear_rows[0]))]
    data_tik['uik'] = [clear_rows[0][i] for i in range(len(clear_rows[0]))]
    data_tik = data_tik[['tik','uik',1,2,3,4,5,6,7,8,9,10,11,12,13,14]]
    return data_tik

list_data_tik = []
for n_tik, link in enumerate(good_links):
    html_tik = get_html(link)
    list_data_tik.append(parse(html_tik,n_tik))

data = pd.concat(list_data_tik,axis=0)