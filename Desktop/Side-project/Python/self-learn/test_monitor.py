import cursor as cursor
import pymysql
from sqlalchemy import create_engine
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import pandas as pd
import re

# -------------------Function & set up-------------------------------------------
now = datetime.datetime.now()
date_time_str = now.strftime("%Y-%m-%d %H")

def cleanStr(str, symbol):
    str = str.replace(symbol, '')
    return str

things = ['monitor']
ts = 1# time sleep value
batchNum = 10


def filter_emoji(desstr, restr=''):
    # 过滤表情
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)

"""
re.sub(pattern, repl, string, count=0, flags=0)
1）函数功能：从左向右把string中能匹配到的字符串，换成repl。将替换后的string返回，如果没有匹配，返回原string。
2）前三个位置参数必写，后两个位置参数是可选参数， pattern 是表达式，string被查找的字符串。

参数repl : 可以是字符串，也可以是函数名。
当是字符串时，匹配到的字符串，都将替换为repl;
当repl 是一个函数的函数名时。此时应是有目的的定义这个函数，而且它的参数只有一个，是匹配到的字符串，并用返回值来替换匹配的字符串。

count : 指定配后替换的最大次数，默认 0 表示替换所有的匹配。

flags，可选标志。如：re.I，re.S , re.M等。
"""



# SQL----------------------------------------------------------------------------


def SQl(queryORtable,db,kind,df_insert="",product=""):
    try:
        db_data = ('mysql+pymysql://' + 'root' + ':' + '@' + '34.67.132.121' + ':3306/'
                  + db + '?charset=utf8')
        engine = create_engine(db_data)

        db_settings = {
            "host": "34.67.132.121",
            "port": 3306,
            "user": "root",
            "password": "",
            "db": db,
            "charset": "utf8"
        }
        conn = pymysql.connect(**db_settings)


        # with conn.cursor() as cursor:
        # cursor.execute(queryORtable)
        # result = cursor.fetchall()


        # if kind =="search":
        #
        #     # with conn.cursor() as cursor:
        #         # cursor.execute(queryORtable)
        #         # result = cursor.fetchall()
        #         # df = pd.dataFrame(result)
        #     df = pd.read_sql(queryORtable, conn)
        #     print(df)

        if kind =="create":

            with conn.cursor() as cursor:
                cursor.execute(
                  'CREATE TABLE ' +'`'+str(date_time_str)+'_'+queryORtable+'` ('+
                  '`id` INT NOT NULL AUTO_INCREMENT,'+
                  '`Brand` VARCHAR(128),'+
                  '`Name` VARCHAR(1028),'+
                  '`Url` VARCHAR(1028),'+
                  '`Price` FlOAT NOT NULL,'+
                  '`Rate` FlOAT NOT NULL,'+
                  '`RateNumber` INT NOT NULL,'+
                  '`Size` VARCHAR(128),'+
                  '`Resolution` VARCHAR(128),'+
                  '`Feature` VARCHAR(4096),'+
                  '`RefreshR` VARCHAR(128),'+
                  '`GlobalRank` VARCHAR(1028),'+
                  '`ViewUrl` VARCHAR(1028),'+
                  '`DFA` VARCHAR(128),' +
                  '`ASIN` VARCHAR(128),' +
                  'PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;'
                )



        if kind == "insert":


            df = df_insert
            print(df)
            # def getdata_str(items):
            #     items_str = ()
            #     n = 0
            #     for i in items:
            #
            #         data = cleanStr(str(i), '"')
            #         if items[0] == i:
            #             items_str.append(data)
            #             n + 1
            #         else:
            #             items_str.append(data)
            #             n + 1
            #     print('----------items_str--------')
            #     print(items_str)
            #     return items_str


            values = []

            for index in range(batchNum):
                i = index+page-(batchNum-1)
                values.append((df.iloc[i,0],df.iloc[i,1],df.iloc[i,2],df.iloc[i,3],df.iloc[i,4]
                               ,cleanStr(str(df.iloc[i,5]),",")
                               ,cleanStr(str(df.iloc[i,6]),",")
                               ,cleanStr(str(df.iloc[i,7]),",")
                              ,cleanStr(str(df.iloc[i,8]),",")
                               ,cleanStr(str(df.iloc[i,9]),",")
                               ,cleanStr(str(df.iloc[i,10]),",")
                               ,str(df.iloc[i,11]),str(df.iloc[i,12])
                                ,str(df.iloc[i,13])))


            # print(values)


            head = 'INSERT INTO '+ db + ".`" +str(date_time_str)+'_'+product+"_Amazon"+"""` (Brand,Name,Url,Price,Rate,RateNumber,Size,Resolution,Feature,RefreshR,GlobalRank,ViewUrl,DFA,ASIN) """\
                    +"""VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""


            print('-------------print query--------------')
            # print(head)
            print(values)
            with conn.cursor() as cursor:
                cursor.executemany(str(head),(values))
                insert = cursor.fetchall()
                conn.commit()
                conn.close()

            print(insert)



        if kind =="check":

            with conn.cursor() as cursor:
                cursor.execute('SHOW TABLES like '+"'"+str(date_time_str)+'_'+queryORtable+"'")
                print('SHOW TABLES like '+"'"+str(date_time_str)+'_'+queryORtable+"'")
            check = cursor.fetchall()
            print(check)
            if len(check) != 0:
                return True
            else:
                return False
    except Exception as err:
        print(err)
        conn.close()
        raise(err)



# Web Scraper---------------------------------------------------------------------

# 自動下載ChromeDriver
service = ChromeService(executable_path=ChromeDriverManager().install())

# 關閉通知提醒


chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("headless")
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--allow-running-insecure-content')
# user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
# chrome_options.add_argument(f'user-agent={user_agent}')


# 開啟瀏覽器


driver = webdriver.Chrome(service=service, chrome_options=chrome_options)
driver.set_window_position(-1500, 0)
driver.maximize_window()
# time.sleep(0.5)  #add lag
test_url = 'https://www.amazon.com/LG-32GN50T-B-Ultragear-Monitor-Compatibility/dp/B08KTN8KFH/ref=sr_1_1?crid=744APWFTWAOV&keywords=LG+32GN50T-B+32-inch+Class+Ultragear+FHD+Gaming+Monitor+with+G-SYNC+Compatibility+%28Renewed%29&qid=1677787651&s=electronics&sprefix=lg+32gn50t-b+32-inch+class+ultragear+fhd+gaming+monitor+with+g-sync+compatibility+renewed+%2Celectronics%2C152&sr=1-1'
# begin scraping------------------------------------------------------------------
try:
    for product in things:

        theurl = []

        theurl.append(test_url)



        # To file array-------------------------------------------------

        brand = []
        title = []
        url = []
        price = []
        star = []
        starNum = []
        size = []
        resolution = []
        feature = []
        refreshR = []
        global_range = []
        view_url = []
        DFA = []
        ASIN = []


        #--------------------------------------------------------------

        # print(theurl)
        for page in range(0,len(theurl)):
            print('第 '+ str(page+1) + ' 個商品')
            #儲存網址
            url.append(theurl[page])

            # 去到你想要的網頁
            driver.get(theurl[page])
            time.sleep(ts)

            driver.execute_script("window.scrollBy(0,8000)")

            checkProduct= driver.find_element(by=By.ID, value='wayfinding-breadcrumbs_feature_div').text
            checkLen = checkProduct.split('\n')
            checkProduct = checkProduct.split('\n')[4]
            # print(len(checkLen))
            if checkProduct == 'Monitors' and len(checkLen) == 5:
                time.sleep(ts)
                #scroll it to middle
                # for i in range(2):
                #     actions = ActionChains(driver)
                #     actions.send_keys(Keys.TAB * 500)
                #     actions.perform()
                #     time.sleep(2.5)

                # 商品名稱----------------------------------------------------------

                title.append(driver.find_element(by=By.ID, value='title').text)
                print(driver.find_element(by=By.ID, value='title').text)
                # 商品定價

                if len(driver.find_elements(by=By.ID, value='corePrice_feature_div')) != 0:
                    getprice = driver.find_element(by=By.ID, value='corePrice_feature_div').text

                elif len(driver.find_elements(by=By.ID, value='corePriceDisplay_desktop_feature_div')) == 0:
                    getprice = driver.find_element(by=By.ID, value='corePrice_desktop').text

                else:
                    getprice = driver.find_element(by=By.ID, value='corePriceDisplay_desktop_feature_div').text

                getprice = getprice.replace('US$', '')  # 先把「US$」拿掉
                if getprice == '':
                    getprice = 0
                elif '\nPrice:\n' in getprice:
                    print(getprice.find('\n'))
                    print(getprice.find('\nPrice:\n'))
                    getprice = getprice[getprice.find('\n')+1:getprice.find('\nPrice:\n')]
                    getprice = getprice.replace('\n', '.')
                    getprice = getprice.replace('$', '')  # 把「定價」拿掉
                else:
                    getprice = getprice.replace(',', '')
                    getprice = getprice.replace('$', '')  # 把「定價」拿掉
                    getprice = getprice.upper()
                    getprice = getprice.replace('PRICE:', '') # 把「定價」拿掉
                    getprice = getprice.replace('FREE RETURNS','')
                    getprice = getprice.replace('FREE RETURN', '')

                    if ' -' in getprice: # 利用「 - 」來切割兩個數字
                        getprice = getprice.replace('\n', '')# 把「US$」拿掉
                        cutlist = getprice.split(' -')
                        getprice = (float(cutlist[0]) + float(cutlist[1]))/2 # 計算平均

                    else:

                        getprice = getprice.replace('\n', '.')
                        getprice = re.sub(r'\(.*?\)', "", str(getprice))
                price.append(float(getprice))
                print(getprice)
            # -------------------------------------------------------------------------------------------------------------

                # 星星評分
                if len(driver.find_elements(by=By.ID, value='acrPopover'))==0:
                    star.append(0)
                else:
                    star.append(driver.find_element(by=By.ID, value='acrPopover').get_attribute("title").replace(' out of 5 stars',''))
                # 全球評分數量
                if len(driver.find_elements(by=By.ID, value='acrCustomerReviewText'))==0:
                    starNum.append(0)
                else:
                    getglobalNum = driver.find_element(by=By.ID, value='acrCustomerReviewText').text
                    getglobalNum = getglobalNum.replace('ratings','')
                    getglobalNum = getglobalNum.replace('rating', '')
                    getglobalNum = getglobalNum.replace(',','')
                    starNum.append(getglobalNum)
                print(star)

            # -------------------------------------------------------------------------------------------------------------

                # 商品描述

                if len(driver.find_elements(by=By.ID, value='productOverview_feature_div')) != 0:
                    getrequest_title = driver.find_elements(by=By.XPATH, value='//td[@class="a-span3"]')
                    getrequest_value = driver.find_elements(by=By.XPATH, value='//td[@class="a-span9"]')
                    getrequest = {}

                    for i in range(len(getrequest_title)):
                        getrequest[getrequest_title[i].text] = getrequest_value[i].text

                    size.append(getrequest.get("Screen Size"))
                    resolution.append(getrequest.get("Display Resolution Maximum"))
                    brand.append(getrequest.get("Brand"))
                    feature.append(getrequest.get("Special Feature"))
                    refreshR.append(getrequest.get("Refresh Rate"))

                else:
                    size.append('N/A')
                    resolution.append('N/A')
                    brand.append('N/A')
                    feature.append('N/A')
                    refreshR.append('N/A')


            # -------------------------------------------------------------------------------------------------------------

                # 產品詳細資訊

                if len(driver.find_elements(by=By.ID, value='productDetails_feature_div')) != 0 \
                        or \
                        len(driver.find_elements(by=By.ID, value='productDetails_db_sections')) != 0:

                    getDetail_title = driver.find_elements(by=By.XPATH,
                                                           value='//th[@class="a-color-secondary a-size-base prodDetSectionEntry"]')
                    getDetail_value = driver.find_elements(by=By.XPATH,
                                                           value='//td[@class="a-size-base prodDetAttrValue"]')
                    getDetail_rank = driver.find_elements(by=By.XPATH,
                                                          value='//td[@class="a-size-base"]')

                    t = len(getDetail_rank)
                    getDetail = {}
                    query = 0
                    print(range(len(getDetail_title)))
                    print(range(len(getDetail_value)))
                    for i in range(len(getDetail_value)):

                        if getDetail_title[i].text == "Customer Reviews" or getDetail_title[
                            i].text == "Best Sellers Rank":
                            # getDetail[getDetail_title[i].text] = getDetail_rank[query].text
                            query = query + 1
                        else:

                            getDetail[getDetail_title[i].text] = getDetail_value[i - query].text

                    # print(getDetail)
                    DFA.append(getDetail.get("Date First Available"))
                    ASIN.append(getDetail.get("ASIN"))

                else:
                    DFA.append("N/A")
                    ASIN.append("N/A")

                # -------------------------------------------------------------------------------------------------------------

                # 全球排名
                if len(driver.find_elements(by=By.ID, value='productDetails_db_sections')) != 0:

                    getdata = driver.find_element(by=By.ID, value='productDetails_db_sections').text
                    getdata = getdata.replace('Best Sellers Rank: ','')
                    # getdata = getdata.replace('\n','')
                    getdata = getdata.split('#')
                    # print(getdata)
                    containar = []
                    for i in range(1,len(getdata)):
                        # print(getdata[i])
                        rang = getdata[i].split(' in ')[0]
                        item = getdata[i].split(' in ')[1]
                        if ' (' in item:
                            item = item.split(' (')[0]
                        # containar[item] = int(rang.replace(',',''))
                        containar.append(item + ' : ' + rang)
                    global_range.append(containar)
                    # print(global_range)
                else:
                    global_range.append('none')



            # -------------------------------------------------------------------------------------------------------------

                # 留言網址
                if len(driver.find_elements(by=By.XPATH, value='//a[@data-hook = "see-all-reviews-link-foot"]'))== 0 :
                    view_url.append('沒有留言')
                else:
                    view_url.append(driver.find_element(by=By.XPATH, value='//a[@data-hook = "see-all-reviews-link-foot"]').get_attribute('href'))


                dic = {
                        'Brand' : brand,
                        'Name' : title,
                        'Url' : url,
                        'Price' : price,
                        'Rate' : star,
                        'RateNumber' : starNum,
                        # 'screenQ' : screenQ,
                        # 'bright' : brightness,
                        # 'pictureQ' : pictureQ,
                        # 'value' : value,
                        # 'gaming' : gaming,
                        'size' : size,
                        'resolution' : resolution,
                        'feature' : feature,
                        'refreshR' : refreshR,
                        'global_range' : global_range,
                        'ViewUrl' : view_url,
                        'DFA' : DFA,
                        'ASIN' : ASIN
                           }
                print(
                        str(len(brand))+'/'\
                        +str(len(title))\
                        +'/'+str(len(url))\
                        +'/'+str(len(star))\
                        +'/'+str(len(starNum))\
                        +'/'+str(len(size))\
                        +'/'+str(len(resolution))\
                        +'/'+str(len(feature))\
                        +'/'+str(len(refreshR))\
                        +'/'+str(len(global_range))\
                        +'/'+str(len(view_url)) \
                        + '/' + str(len(DFA))\
                        + '/' + str(len(ASIN))\
                    )

                # import to database-----------------------------------------------------------------
                #
                #     if (page+1)%2==0:
                #         df_insert = pd.DataFrame(dic)
                #         print(dic)
                #         print(df_insert)
                #         # SQl(product+"Amazon","SelfLearning","create",df_insert)
                #         SQl(product+"_Amazon_test","SelfLearning","insert",df_insert)



                # if (page)%10==(batchNum-1):
                #
                #     df_insert = pd.DataFrame(dic)
                #     # SQl(product+"Amazon","SelfLearning","create",df_insert)
                #     if SQl(product+"_Amazon","SelfLearning","check",) == True:
                #         print("insert data")
                #         SQl(product+"_Amazon","SelfLearning","insert",df_insert,product)
                #
                #     else:
                #         print("create table & insert data")
                #         SQl(product + "_Amazon", "SelfLearning", "create")
                #         SQl(product + "_Amazon", "SelfLearning", "insert", df_insert,product)

            else:
                brand.append('not monitor')
                title.append('not monitor')
                price.append(0)
                star.append(0)
                starNum.append(0)
                size.append('not monitor')
                resolution.append('not monitor')
                feature.append('not monitor')
                refreshR.append('not monitor')
                global_range.append('not monitor')
                view_url.append('not monitor')
                DFA.append('not monitor')
                ASIN.append('not monitor')

        #-------------------------------------------------------------------------------------

        # export csv file---------------------------------------------------------------------
        #
        #     if (page+1)%20==0:
        #         print(str(len(brand)) + "/" + str(len(title)) + "/" + str(len(url)) + "/" + str(len(price)) + "/" + str(len(star)) + "/" + str(len(starNum)) + "/" + str(len(toosmall)) + "/" + str(len(small)) + "/" + str(len(goodsize)) + "/" + str(len(big)) + "/" + str(len(toobig)) + "/" + str(len(size_options)) + "/" + str(len(description)) + "/" + str(len(productDscrp)) + "/"+ str(len(global_range)) + "/" + str(len(view_url)))
        #         print(test)
        #         pd.DataFrame(dic).to_csv(
        #                 product + '_To' +'_'+str(page)+ '_page_Amazon_product_data.csv' , # 檔案名稱
        #                 encoding = 'utf-8-sig', # 編碼
        #                 index=False # 是否保留index
        #                 )
        # pd.DataFrame(dic).to_csv(
        #         'Amazon商品資料.csv', # 檔案名稱
        #         encoding = 'utf-8-sig', # 編碼
        #         index=False # 是否保留index
        #         )
except Exception as er:
    driver.save_screenshot('errorPage.png')
    print(er)
    raise (er)