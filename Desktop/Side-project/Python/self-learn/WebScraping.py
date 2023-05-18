import pandas as pd
from bs4 import BeautifulSoup
import json
import requests
import re



# MOMO購物＿mobile
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
#
# keyword = '除濕機'
# pages = 30
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
# urls = []
# for page in range(1, pages):
#     url = 'https://m.momoshop.com.tw/search.momo?_advFirst=N&_advCp=N&curPage={}&searchType=1&cateLevel=2&ent=k&searchKeyword={}&_advThreeHours=N&_isFuzzy=0&_imgSH=fourCardType'.format(page, keyword)
#     print(url)
#     resp = requests.get(url, headers=headers)
#     if resp.status_code == 200:
#         soup = BeautifulSoup(resp.text)
#         for item in soup.select('li.goodsItemLi > a'):
#             urls.append('https://m.momoshop.com.tw'+item['href'])
#     urls = list(set(urls))
#     print(len(urls))
# #     break
#
# df = []
# for i, url in enumerate(urls):
#     columns = []
#     values = []
#
#     resp = requests.get(url, headers=headers)
#     soup = BeautifulSoup(resp.text)
#     # 標題
#     title = soup.find('meta', {'property': 'og:title'})['content']
#     # 品牌
#     brand = soup.find('meta', {'property': 'product:brand'})['content']
#     # 連結
#     link = soup.find('meta', {'property': 'og:url'})['content']
#     # 原價
#     try:
#         price = re.sub(r'\r\n| ', '', soup.find('del').text)
#     except:
#         price = ''
#     # 特價
#     amount = soup.find('meta', {'property': 'product:price:amount'})['content']
#     # 類型
#     cate = ''.join([i.text for i in soup.findAll('article', {'class': 'pathArea'})])
#     cate = re.sub('\n|\xa0', ' ', cate)
#     # 描述
#     try:
#         desc = soup.find('div', {'class': 'Area101'}).text
#         desc = re.sub('\r|\n| ', '', desc)
#     except:
#         desc = ''
#
#     print('==================  {}  =================='.format(i))
#     print(title)
#     print(brand)
#     print(link)
#     print(amount)
#     print(cate)
#
#     columns += ['title', 'brand', 'link', 'price', 'amount', 'cate', 'desc']
#     values += [title, brand, link, price, amount, cate, desc]
#
#     # 規格
#     for i in soup.select('div.attributesArea > table > tr'):
#         try:
#             column = i.find('th').text
#             column = re.sub('\n|\r| ', '', column)
#             value = ''.join([j.text for j in i.findAll('li')])
#             value = re.sub('\n|\r| ', '', value)
#             columns.append(column)
#             values.append(value)
#         except:
#             pass
#     ndf = pd.DataFrame(data=values, index=columns).T
#     df.append(ndf)
# df = pd.concat(df, ignore_index=True)
# df.info()


# url = "https://www.amazon.com/Apple-MWP22AM-A-cr-AirPods-Renewed/dp/B0828BJGD2/ref=sr_1_5?crid=17ZDJUIVOWUY&keywords=airpods&qid=1663569003&sprefix=airpod%2Caps%2C516&sr=8-5"
url = "https://www.amazon.com/Apple-MWP22AM-A-cr-AirPods-Renewed/dp/B0828BJGD2/"

# HEADERS = {
#     'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64)'
#                    'AppleWebKit/537.36 (HTML, like Gecko)'
#                    'Chrome/44.0.2403.157 Safari/537.36'),
#     'Accept-Language': 'en-US, en;q=0.5'
# }

HEADERS = {
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7',
        'cookie': 'session-id=136-0340723-9192226; session-id-time=2082787201l; i18n-prefs=USD; lc-main=zh_TW; ubid-main=134-3980769-3693765; sp-cdn="L5Z9:TW"; csm-hit=tb:TZMAJPK9WYNJ0Y80TMZK+s-TZMAJPK9WYNJ0Y80TMZK|1660289724778&t:1660289724778&adb:adblk_no; session-token=k3RS++Iksjl7C0tJ6mcNq0RKrVUijnLF3sGiIoxeKYwsG3aTueKJ6BGxf1Z6C+j3R4W9UBC/Jlyv24bO/e4JyDPhLhiKZs64nYY0UmUBqtBsgRAkgHnkzJ4KCI2Soocp46TvfNQe7YzoO/vHjHXoCJ0bVCvhkshLYNLWvkQTSxIJaMYOP3a0Q5rSPnicXs3+54f73HotO2JZaPwBsmnxSVPrGpZpqRNI',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
        }
#
# html = requests.get(url, headers=HEADERS)
# soup = BeautifulSoup(html.text)
#
# title = soup.find('span', {'id': "productTitle"}).text.strip()
# print(title)
# price = soup.find('span', {'id':"renewedBuyBoxPrice"}).text.strip()
# print(price)
#
# rating = soup.find("i",
#                    attrs={'class': 'a-icon a-icon-star a-star-4-5'}).text.strip()
# print(rating+"1")
