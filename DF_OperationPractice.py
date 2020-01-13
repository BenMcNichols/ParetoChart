# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 15:11:33 2020

@author: bmcn6
"""

import matplotlib.pyplot as plt
#%matplotlib inline  #not sure what this line does

import pandas as pd
#import seaborn as sns

excel_file = 'SampleData.xlsx'

df = pd.read_excel(excel_file)
supplierdf = df[df['Supplier'].str.match("Joe's Jam")]  # omits data not from supplier

occurrences = df.groupby('Reason').count().reset_index()  # count number of occurrences of each noncmonformity

print(occurrences)
x = []
y = []
for v in occurrences["Supplier"]:
    x.append(v)
for v in occurrences["Reason"]:
    y.append(v)
print(x)

tmp = occurrences.sort_values("Supplier",ascending=False)
print(tmp)


