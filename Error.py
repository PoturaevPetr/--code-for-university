###Первичная проверка на ошибки с использованием геокодеров Nominatim или ArcGIS
from geopy.geocoders import Nominatim
from geopy.geocoders import ArcGIS
import pandas as pd
df=pd.read_csv("NewBD; Nominatim.csv")
lat=df['lat']
long=df['long']
address=df['address']
geolocator = ArcGIS()
n = 0
k=0
for i in range(len(address)):
    if lat.iloc[i]=='error':
        try:
            location = geolocator.geocode("Пермь, " + address.iloc[i] + "")
            lat.iloc[i] = location.latitude
            long.iloc[i] = location.longitude
        except:
            lat.iloc[i]='error'
            long.iloc[i] = 'error'
            n+=1
            print(n)
    k+=1
    print(k)
df.to_csv("NewBD; Nominatim.csv")
print(df)

