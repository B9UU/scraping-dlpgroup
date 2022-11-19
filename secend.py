import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

def req(url):
    headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
        }

    res = requests.get(url,headers=headers)
    dd = bs(res.content, 'html.parser')
    return dd

bb = dict()
page = req('https://www.dplgroup.com/all-products/')
fil = page.find_all('div', class_='wpc-term-item-content-wrapper')
for i in fil:
    import json
    with open('result.json', 'w') as fp:
        json.dump(bb, fp)
    ss = req(i.find('a')['href'])
    next = True
    while next:
        title = ss.find_all('a',attrs={'rel':'bookmark'})
        tkhar = ss.find_all('span',class_='wpc-chip-content')[1].find('span',class_='wpc-filter-chip-name').text
        for ch in title:
            
            try:
                bb[ch.text].append(tkhar)
            except KeyError:
                bb[ch.text] = list()
                bb[ch.text].append(tkhar)
        if ss.find('a', class_='page-numbers nav-next'):
            try:
                ss = req(ss.find('a', class_='page-numbers nav-next')['href'])
            except:
                next = False
        else:
            next = False

mn = pd.read_csv('dplgroup-data.csv').to_dict('records')

for er in mn:
    name = bb[er['Title']]
    er['tags'] = er['tags'].join([f"{dbl} " for dbl in name])


dds =pd.DataFrame(mn)
dds.to_csv('data2.csv',index=False)
        
