import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gdown 

# url = 'https://drive.google.com/uc?id=1LALbA30NdFeOZxe06iYSUlQEDCPyDDpY'
# output = 'recent-grads.csv'
# gdown.download(url, output, quiet=False)

# --------------------------------------------------------------

# loading data to DataFrame
df = pd.read_csv("recent-grads.csv")
print(df)
df.info()
# --------------------------------------------------------------


# 檢視[排名1至173的科系]的[收入]變化

# plot預設是畫折線圖

df.plot(x="Rank", y=["P25th", "Median", "P75th"])
plt.show()

# --------------------------------------------------------------

# 檢視[系所收入中位數]與[失業人數比例]的關係

# 將 plot 裡的 kind 參數設為 scatter 就能畫出散佈圖
#
df.plot(x="Median", y="Unemployment_rate", kind="scatter")
df.plot(x="Median", y="Unemployment_rate")
plt.show()

# --------------------------------------------------------------
# 檢視[收入中位數前五名的科系]，在[收入中位數]上的差異
#
# 將 plot 裡的 kind 參數設為 bar 就能畫出長條圖

df.sort_values(by="Median", ascending=False).head()
top_5 = df.sort_values(by="Median", ascending=False).head(10)

top_5.plot(x="Major", y="Median", kind="bar", fontsize=10)
plt.show()

# --------------------------------------------------------------
# 檢視[收入中位數超過6萬的科系]，在[收入]上的差異
#
# top_medians = df[df["Median"] > 60000].sort_values("Median")
#
# top_medians.plot(x="Major", y=["P25th", "Median", "P75th"], kind="bar")
# plt.show()

# --------------------------------------------------------------
# 檢視[不同科系類群]在[收入中位數]上的差異

# 將 plot 裡的 kind 參數設為 barh 就能畫出水平長條圖

# cat_medians = df.groupby("Major_category")["Median"].mean().sort_values()
# cat_medians = df.groupby("Major_category")["Median"].mean().sort_values()
#
# cat_medians.plot(kind="barh", fontsize=10)
# plt.show()

# --------------------------------------------------------------
#
test_correlation= df.corr(x="Median", y="Unemployment_rate", kind="scatter")
plt.show()