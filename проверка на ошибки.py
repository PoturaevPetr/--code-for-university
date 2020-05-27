##Количество ошибок
import pandas as pd
df=pd.read_csv("NewBD; Nominatim.csv")
lat=df['lat']
n=0
for i in lat:
    if i=='error' or i=='Error':
        n+=1
print(n)
