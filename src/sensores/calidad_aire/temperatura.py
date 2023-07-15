from machine import Pin, I2C, sleep
import mpu6050 #Modulo de trabajo de Gyroscopio o acelerometro
import time
i2c = I2C(scl=Pin(22), sda=Pin(21))  #initializing the I2C method for ESP32

ledRojo= Pin(13, Pin.OUT)  # Pin del Led Rojo
ledAzul=Pin(14, Pin.OUT)  # Pin del Led Blue
ledNaranja=Pin(26,Pin.OUT)  # Pin del Led Green

mpu= mpu6050.accel(i2c)

while True:  
  
  temps =(mpu.get_values())

  tem=temps["Tmp"] # Temperatura
  print(tem)
  time.sleep(1)

  if tem > 39:
    print(" La temperatura está muy alta", tem)
    ledRojo.value(1)
    time.sleep(2)
    ledRojo.value(0)

  elif tem == 38:
    print("La temperatura es Normal", tem)
    ledAzul.value(1)
    time.sleep(2)
    ledAzul.value(0)

  elif tem < 37:
    print("La temperatura es muy baja", tem)
    ledNaranja.value(1)
    time.sleep(2)
    ledNaranja.value(0)
    time.sleep(1)
