import network, time, urequests
from machine import Pin
from utime import sleep, sleep_ms
from dht import DHT22
import ujson
import ufirebase as firebase

s_dht = DHT22(Pin(15))


def conectaWifi(red, password):
    global miRed
    miRed = network.WLAN(network.STA_IF)
    if not miRed.isconnected():  # Si no está conectado…
        miRed.active(True)  # activa la interface
        miRed.connect(red, password)  # Intenta conectar con la red
        print('Conectando a la red', red + "…")
        timeout = time.time()
        while not miRed.isconnected():  # Mientras no se conecte..
            if (time.ticks_diff(time.time(), timeout) > 10):
                return False
    return True


if conectaWifi("FAMILIA ALVIS 2G", "Mapis201"):

    print("Conexión exitosa!")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())

    firebase.setURL("https://cyberdog-cfc41-default-rtdb.firebaseio.com/")

    while True:
        # >>> DHT22 <<<<<
        s_dht.measure()
        tem = s_dht.temperature()
        hum = s_dht.humidity()
        print("T:{} c   H:{}% ".format(tem, hum))
        sleep_ms(60)
        message = {"Temperatura": tem, "Humedad": hum}
        firebase.put("cyberdog/sensor_dht22", message, bg=0)
        print("Mensaje Enviado")

        firebase.get("cyberdog/sensor_dht22", "dato", bg=0)
        print("Dato recuperado: " + str(firebase.dato))

        # >>> 

else:
    print("Imposible conectar")
    miRed.active(False)
