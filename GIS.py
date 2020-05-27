###Обработка исходной БД. Получение координат по конкретным адресам с использованием  Nominatim (ArcGIS менее точен для геокодирования по России)
import folium
from geopy.geocoders import Nominatim
from geopy.geocoders import ArcGIS
import pandas as pd
#import geopy
df=pd.read_csv("perm_1.csv")
#df=df[:20]
adres=df["address"]
geolocator = Nominatim()
n=0
LAT=[]
LONG=[]
for i in adres:
    try:
        location = geolocator.geocode("Пермь, "+i+"")
        lat=location.latitude
        long=location.longitude
        LAT.append(lat)
        LONG.append(long)
    except:
        print("ERROR:"+i)
        LAT.append("error")
        LONG.append("error")
    n+=1
    print(n)
    print(lat, long)
print(LAT)
df['lat']=LAT
df['long']=LONG
df.to_csv("NewBD; Nominatim.csv")
print(df)






