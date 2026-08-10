from ucimlrepo import fetch_ucirepo
import pandas as pd 
import sqlite3

dataset = fetch_ucirepo(id=863)
X = dataset.data.features #input variables
y = dataset.data.targets #risk level (target variable) low, mid, high

print(X.head())  #print first 5 rows of the input variables
print(X.shape) #print the shape of the input variables


print(y.value_counts()) #print the number of samples for each risk level

df = pd.concat([X,y], axis=1)  #combine input variables and target variable into a single df

#connect to sqlite database
conn = sqlite3.connect("data/maternal_health_risk.db")
df.to_sql("maternal_health_risk", conn, if_exists="replace", index=False) #save the df to the database
conn.close()

