import numpy as np
import pandas as pd
from pandas import Series, DataFrame
from numpy.random import randn
# Stats
from scipy import stats
# Plotting
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
#Create a random normal-dist dataset
dataset1 = randn(100)

#Plot a histogram of the dataset, note bins=10 by default
plt.hist(dataset1)

# Lets make another dataset
dataset2 = randn(80)

#Plot
plt.hist(dataset2,color='indianred')