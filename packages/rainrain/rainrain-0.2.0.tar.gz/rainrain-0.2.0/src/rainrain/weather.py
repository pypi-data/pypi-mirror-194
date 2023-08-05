import requests
import json
from datetime import datetime
import time


def find():
    x=input('enter district name: ')
    print('searching.............')
    
    x=x.lower()
    url='https://api.openweathermap.org/data/2.5/weather?q={}&APPID=0720f6e1ee8175e215f55550f28f6945'.format(x)
    main=requests.get(url)
    data=main.json()
    time.sleep(1)
    longitude=data['coord']["lon"]
    latitude=data['coord']["lat"]
    desc=data["weather"][0]["description"]
    temp=data['main']["temp"]-273
    temp=f'{temp} deg celsius'
    name=data['name']
    humidity=data['main']["humidity"]
    humid=f'{humidity}%'
    a=f'Longitude = {longitude}'
    b=f'Latitude={latitude}'
    c=f'location= {name}'
    d=f'temperature = {temp}'
    e=f'humidity={humid}'
    f=f'status ={desc}'
    print(c,a,b,d,e,f,sep='\n')
    print("Thanks for using prajil's service")
    print('--------Finished---------')


