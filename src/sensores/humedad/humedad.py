from dht import DHT22
from machine import Pin # pines 
from utime import sleep

sensorDHT = DHT22(Pin(15))

while True:

    sleep(1)
    sensorDHT.measure()
    temp = sensorDHT.temperature()
    hum = sensorDHT.humidity()
    kel = temp + 273
    far = (temp*5)/9 + 32
    print("T={:02}C H={:02}%  K={:02}K  F= {:02}F".format(temp, hum, kel, far))

    if temp >= 25: 
        print ("Peligro temperatura muy caliente")    
    elif temp>= 22 and temp <= 24:
        print("La temperatura del agua esta normal o bien") 
    elif temp <= 21:
        print("Esta muy fria")