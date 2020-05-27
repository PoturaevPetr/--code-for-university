####Устранение ошибок с использованием API Google
import pandas as pd
from selenium import webdriver
df=pd.read_csv("NewBD; Nominatim.csv")
lat=df['lat']
long=df['long']
address=df['address']
#df.address = df.address.str.replace('/', ' ')
url=['https://www.google.com/maps/search/Пермь ' + i for i in address]
option = webdriver.ChromeOptions()
prefs = {'profile.default_content_setting_values': {'images': 2, 'javascript': 2}}
option.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome("C:\\Users\\User\\Desktop\\chromedriver.exe", options=option)
n=0
for i in range(len(address)):
    if lat.iloc[i]=='error':
        driver.get(url[i])
        URL=driver.find_element_by_css_selector('meta[itemprop=image]').get_attribute('content')
        lat.iloc[i] = URL.split('?center=')[1].split('&zoom=')[0].split('%2C')[0]
        long.iloc[i] = URL.split('?center=')[1].split('&zoom=')[0].split('%2C')[1]
        n+=1
        print(lat.iloc[i])
driver.close()
df.to_csv("NewBD; Nominatim.csv")
