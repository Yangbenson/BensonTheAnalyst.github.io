import cursor as cursor
import pymysql
from sqlalchemy import create_engine
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
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

things = ["shirt",'t shirt']
ts = 0# time sleep value
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
                  '`Brand` VARCHAR(1028),'+
                  '`Name` VARCHAR(1028),'+
                  '`Url` VARCHAR(1028),'+
                  '`Price` FlOAT NOT NULL,'+
                  '`Rate` FlOAT NOT NULL,'+
                  '`RateNumber` INT NOT NULL,'+
                  '`Toosmall` INT NOT NULL,'+
                  '`Small` INT NOT NULL,'+
                  '`Fit` INT NOT NULL,'+
                  '`Big` INT NOT NULL,'+
                  '`Toobig` INT NOT NULL,'+
                  '`Sizes` VARCHAR(4096),'+
                  '`Colors` VARCHAR(4096),'+
                  '`Description` VARCHAR(4096),'+
                  '`ProductDscrp` VARCHAR(4096),'+
                  '`GlobalRank` VARCHAR(1028),'+
                  '`ViewUrl` VARCHAR(1028),'+
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
                print(type(df.iloc[i]))
                values.append((df.iloc[i,0],df.iloc[i,1],df.iloc[i,2],df.iloc[i,3],df.iloc[i,4]
                               ,cleanStr(str(df.iloc[i,5]),",")
                               ,cleanStr(str(df.iloc[i,6]),",")
                               ,cleanStr(str(df.iloc[i,7]),",")
                              ,cleanStr(str(df.iloc[i,8]),",")
                               ,cleanStr(str(df.iloc[i,9]),",")
                               ,cleanStr(str(df.iloc[i,10]),",")
                               ,str(df.iloc[i,11])
                               ,str(df.iloc[i,12])
                               ,df.iloc[i,13]
                              ,df.iloc[i,14],
                               str(df.iloc[i,15])
                               ,df.iloc[i,16]))

            # print(values)


            head = 'INSERT INTO '+ db + ".`" +str(date_time_str)+'_'+product+"_Amazon"+"""` (Brand,Name,Url,Price,Rate,RateNumber,Toosmall,Small,Fit,Big,Toobig,Sizes,Colors,Description,ProductDscrp,GlobalRank,ViewUrl) """\
                    +"""VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""


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

# begin scraping------------------------------------------------------------------
try:
    for product in things:

        theurl = []
        driver.get("https://www.amazon.com/s?k=" + product + "&page=0" +  "ref=sr_pg_0")

        for i in range(2):

            # 去到你想要的網頁
            # driver.get("https://www.amazon.com/s?k="+ product +"&page="+ str(i) +"ref=sr_pg_"+str(i))

            geturl = driver.find_elements(by=By.XPATH, value='//h2/a')
            # print(geturl)
            for j in geturl:
                theurl.append(j.get_attribute('href'))

            findNP = driver.find_element(by=By.XPATH
                                         , value='//span[@class = "s-pagination-strip"]/a[@class = "s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]')
            nextPage = findNP.get_attribute('href')
            print(nextPage)
            driver.get(nextPage)

        # To file array-------------------------------------------------

        brand = []
        title = []
        url = []
        price = []
        star = []
        starNum = []
        toosmall = []
        small = []
        goodsize = []
        big = []
        toobig = []
        size_options = []
        color_options = []
        description = []
        productDscrp = []
        global_range = []
        view_url = []


        #--------------------------------------------------------------
        # print(theurl)
        for page in range(0,len(theurl)):
            print('第 '+ str(page+1) + ' 個商品')
            #儲存網址
            url.append(theurl[page])

            # 去到你想要的網頁
            driver.get(theurl[page])
            time.sleep(ts)

            # 品牌名稱
            if len(driver.find_elements(by=By.ID, value='bylineInfo')) == 0 :
                getbrand = driver.find_element(by=By.ID, value='bylineInfo_feature_div').text
                getbrand = getbrand.replace('Visit the ', '')  # remove Visit the
                getbrand = getbrand.replace('Store', '')  # remove Store
                getbrand = getbrand.replace('\n', '')
                brand.append(getbrand)
            else:
                getbrand = driver.find_element(by=By.ID, value='bylineInfo').text
                getbrand = getbrand.replace('Visit the ', '') #remove Visit the
                getbrand = getbrand.replace('Store', '') #remove Store
                brand.append(getbrand)

            # 商品名稱
            title.append(driver.find_element(by=By.ID, value='title').text)

            # 商品定價
            if len(driver.find_elements(by=By.ID, value='corePriceDisplay_desktop_feature_div')) == 0:
                getprice = driver.find_element(by=By.ID, value='corePrice_desktop').text

            elif len(driver.find_elements(by=By.ID, value='corePrice_feature_div')) != 0:
                getprice = driver.find_element(by=By.ID, value='corePrice_feature_div').text

            else:
                getprice = driver.find_element(by=By.ID, value='corePriceDisplay_desktop_feature_div').text

            getprice = getprice.replace('US$', '')  # 先把「US$」拿掉
            if '有了交易' in getprice:
                getprice = getprice[getprice.find('有了交易')+6:]
                getprice = getprice.split('\n')[0]
            elif '\nPrice:\n' in getprice:
                getprice = getprice[getprice.find('\n')+1:getprice.find('\n定價:\n')]
                getprice = getprice.replace('\n', '.')
            else:

                getprice = getprice.replace('Price:', '') # 把「定價」拿掉
                getprice = getprice.replace('$', '')  # 把「定價」拿掉
                getprice = getprice.replace('Free Returns on some sizes and colors','')
                getprice = getprice.replace('Free Return on some sizes and colors', '')
                if ' -' in getprice: # 利用「 - 」來切割兩個數字
                    getprice = getprice.replace('\n', '')# 把「US$」拿掉
                    cutlist = getprice.split(' -')
                    getprice = (float(cutlist[0]) + float(cutlist[1]))/2 # 計算平均
                else:
                    getprice = getprice.replace('\n', '')
            price.append(getprice)
            # print(getprice)
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
            # print(star)
        # ------------------------------------------------------------------------------------
            # 客戶回饋大小
            if len(driver.find_elements(by=By.ID, value='fitRecommendationsLinkRatingText')) == 0:
                toosmall.append(0)
                small.append(0)
                goodsize.append(0)
                big.append(0)
                toobig.append(0)
            else:


                time.sleep(ts)
                driver.find_element(by=By.ID, value='fitRecommendationsLinkRatingText').click()
                time.sleep(ts)
                getrequest = driver.find_elements(by=By.XPATH, value='//td[@class = "a-span1 a-nowrap"]')
                # print(getrequest[0].text+"/"+getrequest[1].text+"/"+getrequest[2].text+"/"+getrequest[3].text+"/"+getrequest[4].text)
                toosmall.append(cleanStr((getrequest[0].text),','))# 太小
                small.append(cleanStr((getrequest[1].text),','))# 有點小
                goodsize.append(cleanStr((getrequest[2].text),','))# 尺寸正確
                big.append(cleanStr((getrequest[3].text),','))# 有點大
                toobig.append(cleanStr((getrequest[4].text),','))# 太大
                # 關閉選項
                # if len(driver.find_elements(by=By.XPATH, value='//button[@data-action = "a-popover-close"]')) != 0:
                #     driver.find_element(by=By.XPATH, value='//button[@data-action = "a-popover-close"]').click()
                # time.sleep(ts)
         # -------------------------------------------------------------------------------------------------------------

            # 大小選項
            containar = []

            if len(driver.find_elements(by=By.ID, value='variation_size_name')) == 0:
                size_options.append('one size')

            else:
                driver.find_element(by=By.XPATH, value='//span[@data-csa-interaction-events="click"]').click()
                time.sleep(ts)

                for i in driver.find_elements(by=By.XPATH, value='//li[contains(@id, "size_name_")]'):
                    if i.text != 'Select' and i.text != '':
                        containar.append(i.text)
                size_options.append(containar)

        # -------------------------------------------------------------------------------------------------------------

            # 顏色選項
            containar = []
            for i in driver.find_elements(by=By.XPATH, value='//li[contains(@id, "color_name_")]'):
                getdata = i.get_attribute("title")
                containar.append(getdata.replace('Click to select ','')) # 取代掉「請按下選擇」
            color_options.append(containar)

        # -------------------------------------------------------------------------------------------------------------

            # 商品描述
            if len(driver.find_elements(by=By.ID, value='productDescription')) != 0:
                # print(driver.find_elements(by=By.ID, value='productDescription'))
                # print(len(driver.find_elements(by=By.ID, value='productDescription')))
                productDscrp.append(filter_emoji(driver.find_element(by=By.ID, value='productDescription').text))
            else:
                productDscrp.append('none')


        # -------------------------------------------------------------------------------------------------------------

            # 產品詳細資訊

            if len(driver.find_elements(by=By.ID, value='detailBullets_feature_div')) != 0:
                description.append(driver.find_element(by=By.ID, value='detailBullets_feature_div').text)
                # 全球排名
                # print(getdata)
                getdata = driver.find_element(by=By.XPATH, value='//div[@id = "detailBulletsWrapper_feature_div"]/ul').text
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
                description.append('none')



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
                    'Toosmall' : toosmall,
                    'Small' : small,
                    'Fit' : goodsize,
                    'Big' : big,
                    'Toobig' : toobig,
                    'Sizes' : size_options,
                    'Colors' : color_options,
                    'Description' : description,
                    'ProductDscrp' : productDscrp,
                    'GlobalRank' : global_range,
                    'ViewUrl' : view_url
                   }

        # import to database-----------------------------------------------------------------
        #
        #     if (page+1)%2==0:
        #         df_insert = pd.DataFrame(dic)
        #         print(dic)
        #         print(df_insert)
        #         # SQl(product+"Amazon","SelfLearning","create",df_insert)
        #         SQl(product+"_Amazon_test","SelfLearning","insert",df_insert)



            if (page)%10==(batchNum-1):

                df_insert = pd.DataFrame(dic)
                # SQl(product+"Amazon","SelfLearning","create",df_insert)
                if SQl(product+"_Amazon","SelfLearning","check",) == True:
                    print("insert data")
                    SQl(product+"_Amazon","SelfLearning","insert",df_insert,product)

                else:
                    print("create table & insert data")
                    SQl(product + "_Amazon", "SelfLearning", "create")
                    SQl(product + "_Amazon", "SelfLearning", "insert", df_insert,product)





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