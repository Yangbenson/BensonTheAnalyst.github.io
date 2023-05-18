import pymysql
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import time
import datetime

# -------------------Function & set up-------------------------------------------

def cleanStr(str, symbols=[]):

    for i in symbols:
        str = str.replace(i, '')
    return str

table = "2023-03-02 15_monitor&i=computer_Amazon"

def str2List(data = pd.DataFrame(),column=[]): #change df column from Str to List

    df = data
    for i in column:#detect the column have to be change

        list = []

        for j in df.iloc[:,i]: # pull out each of the column

            data = cleanStr(j, ["[", "]", "'"])
            data = data.split(",")
            list.append(data)

        df.iloc[:, i] = list

    return df


def cleanData_float(data=pd.DataFrame(), column=[], refer=[]):  # change df column from Str to List

    df = data
    for i in column:#detect the column have to be change

        list = []
        print(df.iloc[:, i])
        for j in df.iloc[:,i]: # pull out each of the column

            data = cleanStr(j, refer)
            if data == 'None':
                list.append(0)
            else:
                list.append(data)
        df.iloc[:, i] = list

    return df


# SQL----------------------------------------------------------------------------


def SQl(queryORtable,db):
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


        with conn.cursor() as cursor:
            cursor.execute(queryORtable)
            result = cursor.fetchall()
            df = pd.DataFrame(result)
            conn.commit()
            conn.close()
            return df

    except Exception as err:
        print(err)
        conn.close()
        raise(err)


# ----------------------------------------------------------------------------------------
# df = SQl('select `Name`,`Price`,`Rate`,`Sizes`,`Colors` from `2023-02-21 11_sweatpant_Amazon`','SelfLearning')
# df = str2List(df, [3, 4])

 # check tables---------------------------------------------------------------------------

# print(df.shape[0])
# print(df)
# print(df.iloc[0,0])

# for i in range(df.shape[0]):
#     print(df.iloc[i])
#     tables.append(df.iloc[i, 0])
# print(tables)


df = SQl('select `Price`,`Rate`,`Size`,`RefreshR`,`RateNumber`,`Resolution` from `'+table+'`','SelfLearning')
df.columns = ['Price','Rate','Size','RefreshR','RateNumber','Resolution']
print(df)
# df = cleanData_float(df, [2],[" Inches", "Feet"])
# df = cleanData_float(df, [3],[" Hz"])
# df['Size'] = df['Size'].apply(lambda x: x != 'none')
# df.to_csv(
#         'Debug.csv', # 檔案名稱
#         encoding = 'utf-8-sig', # 編碼
#         index=True # 是否保留index
#         )
# df.replace(to_replace='none', value=None).dropna()
df = df[df['Size'].map(lambda x: x.isdigit())]
print(df)

df.replace(to_replace='none', value=pd.NA).dropna(axis=0, subset=['Size'])
df.replace(to_replace='none', value=pd.NA).dropna(axis=0, subset=['RefreshR'])

print('--------')
print(df)
# df = cleanData_float(df, [2],[" Inches", "Feet"])
# df = cleanData_float(df, [3],[" Hz"])

# df['Size'] = df['Size'].apply(lambda x: x != 'none')
df['RefreshR'] = df['RefreshR'].apply(lambda x: x != 'none')


df = df.astype({"Size":'float64'})
df = df.astype({"RefreshR":'float64'})

# scatter chart

print(df)
# df.info()
df_n_OL = df[df.Price < 10000]
# df_n_OL.plot(x=0, y=4, kind="scatter")
# sns.lmplot(data=df_n_OL, x='Price', y='Rate', fit_reg=True)


# correlation chart

print(df.corr())
# plt.matshow(df.corr())
# plt.show()

# --------matplot-----------

df_brand = SQl('select `Brand`,AVG(`Rate`),AVG(`Price`),AVG(`RateNumber`) from `'+table+'`'
                + 'GROUP BY Brand '
                # + 'HAVING AVG(`Rate`)>4.5 '
                # + 'ORDER BY AVG(`Rate`) DESC '
               , 'SelfLearning')
df_brand.columns = ['Brand','Rate','Price','RateNumber']
# print(df_brand)
X = df_brand["Brand"]
Y = df_brand["Rate"]
print(df_brand.corr())
plt.scatter(X, Y)

plt.title("Brand / Rate")
plt.xlabel("Brand")
plt.ylabel("Rate")
# df_brand.plot(x=0, y=3, kind="scatter")
sns.lmplot(data=df_brand, x='Price', y='Rate', fit_reg=True)
plt.show()











