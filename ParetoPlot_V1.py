# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 13:43:02 2020

@author: bmcn6

Create and style a pareto chart from a list of nonconformities and nonconformity sources.

Sources:
    https://tylermarrs.com/posts/pareto-plot-with-matplotlib/
"""


import matplotlib.pyplot as plt
#%matplotlib inline  #not sure what this line does
import matplotlib.cm as cm

import pandas as pd
#import seaborn as sns

excel_file = 'SampleData.xlsx'

df = pd.read_excel(excel_file)

"""df = pd.DataFrame({
    'Flavor': ['Chocolate', 'Vanilla', 'Mint', 'Swirl', 'Nut'],
    'Orders': [1500,  670,  950,  450,   75]
})"""

#print(supplierdf.head())  # Helpful glance at data
                  # You should really start remembering this one

def pareto_plot(df, x=None, y=None, customer = None, show_pct_y=False, pct_format='{0:.0%}',saveas = None):
    plt.style.use("seaborn")
    title = "Nonconformities by Cause"
    if customer != None:
        df = df[df['Supplier'].str.match(customer)]  # omits data not from supplier
        title = customer + " Nonconformities by Cause"
    occurrences = df.groupby('Reason').count().reset_index()  # count number of occurrences of each nonconformity
    print(df.head())
    ylabel = "Occurrences"
    tmp = occurrences.sort_values(y, ascending=False)
    x = tmp[x].tolist()
    y = tmp[y].tolist()
    print(x)
    print(y)
    #x = tmp[x].values
    #y = tmp[y].values
    
    # at this point, x should be an ordered list of x axis categories
    # and y should be the number of occurrences
    #weights = y / y.sum()

    weights = []
    colorList = []
    for count in y:
        weights.append(count/sum(y))
    for count in weights:
        colorList.append(count+(1-max(weights)))
    print(weights)
    print(colorList)
    cumsum = []
    for counter,percent in enumerate(weights):
        cumsum.append(sum(weights[:counter+1]))
    fig, ax1 = plt.subplots()
    my_cmap = cm.get_cmap("Blues")
    ax1.bar(x, y,color=my_cmap(colorList))
    #ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    ax1.set_ylim([0,max(y)+1])

    ax2 = ax1.twinx()
    ax2.plot(x, cumsum, '-s',color = "black")#, alpha=0.5)
    ax2.set_ylabel('', color='purple')
    ax2.tick_params('y')#, colors='purple') #right y axis label color
    ax2.set_ylim([0,1.05])
    ax2.grid(alpha = 0)
    
    vals = ax2.get_yticks()
    ax2.set_yticklabels(['{:,.0%}'.format(x) for x in vals])

    # hide y-labels on right side
    if not show_pct_y:
        ax2.set_yticks([])
    
    formatted_weights = [pct_format.format(x) for x in cumsum]
    bbox_props = dict(boxstyle="round,pad=0.5", fc="w", ec="0", lw=2)
    for i, txt in enumerate(formatted_weights):
        ax2.text(x[i], cumsum[i],txt, verticalalignment="center",bbox=bbox_props)    
    plt.title(title,fontsize = 14)
    
    plt.tight_layout()
    plt.show()
    if saveas != None:
        fig.savefig(saveas, dpi=500)

#pareto_plot(df, x='Reason', y='Supplier', customer="Joe's Jam",show_pct_y=True,saveas="testfig.png")    

pareto_plot(df, x='Reason', y='Supplier', show_pct_y=False,saveas="Combined Pareto.png")

for count,customer in enumerate(df["Supplier"].unique().tolist()):
    savename = customer+" Pareto.png"
    print(savename)
    pareto_plot(df, x='Reason', y='Supplier', customer=customer,show_pct_y=False,saveas=savename)