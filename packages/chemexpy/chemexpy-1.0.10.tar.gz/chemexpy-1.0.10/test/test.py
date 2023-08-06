#test

import pandas as pd
import chemexpy as ch

data=pd.read_csv("data_1.csv")
print(data.head())

#run functions

data=ch.data_prep(data, "Type")

corr=ch.correlation_plot(data,"MW","TSPA","AP","HBD_count","HBA_count")
print(corr.head())
#perform multiple feature assessment
ch.feature_plot(data,"MW","TSPA","AP","HBD_count","HBA_count")
#check the normality of data distribution
ch.normality_check(data,"MW")
