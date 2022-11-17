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

# def extracting_data(page):
#     data = {
#         'Category':page.find('span', attrs={'class':'posted_in'}).text,
#         'tags': page.find('span', class_='tagged_as')['href'] if page.find('span', class_='tagged_as') else '',
#         'Title': page.find('h1',class_='product_title entry-title').text,

#         }

# page = req()
#     dic = page.find_all('a', attrs={'rel':'bookmark'})
    
# ju = dd.find('a',class_='page-numbers nav-next')
# if ju:
#     print('yes')
li = pd.read_csv('data.csv').to_dict('records')
lo = pd.read_csv('data.csv')['Product Url'].values.tolist()
# li =list()
for num in range(1,10):
    if num == 1:
        url = f"https://www.dplgroup.com/all-products/"
    else:
        url = f"https://www.dplgroup.com/all-products/page/{num}/"
    page = req(url)
    dic = page.find_all('a', attrs={'rel':'bookmark'})
    for product in dic:
        if product['href'] in lo:
            print('all ready')
            continue
        details = req(product['href'])
        print(product['href'])
        product_details = details.find('table',class_='product-tab-table').find('tbody').find_all('tr')
        standard_data = details.find_all('div',class_='uvc-sub-heading ult-responsive')[1]
        data = {
        'Category':details.find('span', attrs={'class':'posted_in'}).text,
        'tags': details.find('span', class_='tagged_as').find('a')['href'] if details.find('span', class_='tagged_as') else '',
        'Title': details.find('h1',class_='product_title entry-title').text,
        'Product Url': product['href'],
        'Features': details.find('ul',class_='product-features').text,
        'Images Url': ''.join([f"{img.get('src')} " for img in details.find_all('img', class_='attachment-thumbnail size-thumbnail')]),
        'Standards - Text': standard_data.find('ul').text if standard_data.find('ul') else '',
        'Standards - Icons Urls': ''.join([f"{img.get('src')} " for img in standard_data.find_all('img')]),
        'Applications' : details.find_all('div',attrs={'class':'uvc-sub-heading ult-responsive'})[2].find('ul').text,
        'Download Documments': ''.join([f"{dow['href']} " for dow in details.find_all('a', class_='product-download-btn')])
        }
        print(data['Images Url'])
        for each in product_details:
            if each.find_all('td')[0].text.strip() == 'Ratings':
                data['Product Details - Ratings Icons'] = ''.join([f"{img.get('src')} " for img in each.find_all('td')[1].find_all('img') if each.find_all('td')[1].find_all('img') ])
                data['Product Details - Text'] = each.find_all('td')[1].text
            else:
                data[f"Product Details - {each.find_all('td')[0].text.strip()}"] = each.find_all('td')[1].text.strip()
        try:
            data['Primary Industries Icones'] = ''.join([f"{img.get('src')} " for img in details.find('div',class_='woocommerce-product-details__short-description').find('p').find_all('img')])
        except AttributeError:
            ''
        li.append(data)
        dd =pd.DataFrame(li)
        dd.to_csv('data.csv',index=False)
    

