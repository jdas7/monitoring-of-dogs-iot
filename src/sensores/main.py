import network, time, urequests
from machine import Pin, ADC
from utime import sleep, sleep_ms, ticks_ms
from dht import DHT22
import ufirebase as firebase


# Pin de sensores
pin_dht22 = 15
pin_mq135 = 34
pin_ritmo = 32

# Crear una lista para almacenar los valores del sensor
datos_sensor = []

# Variables para el cálculo del ritmo cardíaco
ultima_muestra = 0
tiempo_entre_latidos = 0
ritmo_cardiaco = 0


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


def obtener_temperatura_humedad():
    s_dht = DHT22(Pin(pin_dht22))
    s_dht.measure()
    temperatura = s_dht.temperature()
    humedad = s_dht.humidity()
    return temperatura, humedad


def obtener_concentracion_gas():
    adc = ADC(Pin(pin_mq135))
    adc.atten(ADC.ATTN_6DB)
    adc.width(ADC.WIDTH_12BIT)

    valores = []
    for _ in range(50):  # Realizamos 50 lecturas para obtener un promedio
        valores.append(adc.read())
        sleep_ms(10)

    promedio = sum(valores) / len(valores)

    # Ajuste del valor según la sensibilidad del sensor y la concentración de gas
    # Este ajuste puede variar según el modelo específico del MQ-135 y el ambiente
    concentracion_gas = (promedio / 4095.0) * 100.0

    return concentracion_gas


def obtener_voltaje():
    s_xd = ADC(Pin(pin_ritmo))
    s_xd.atten(ADC.ATTN_6DB)
    s_xd.width(ADC.WIDTH_12BIT)

    valor = s_xd.read()
    voltaje = (3.3/((2**12)-1))*valor
    return voltaje


def calcular_ritmo_cardiaco():
    global datos_sensor, ultima_muestra, tiempo_entre_latidos, ritmo_cardiaco


    # Leer el voltaje del sensor
    voltaje = obtener_voltaje()

    # Almacenar el valor del sensor en la lista
    datos_sensor.append(voltaje)

    # Verificar si hay picos en la señal (implementación no incluida en este ejemplo)

    # Calcular el tiempo entre latidos en milisegundos
    tiempo_actual = ticks_ms()
    if ultima_muestra != 0:
        tiempo_entre_latidos = tiempo_actual - ultima_muestra

    # Actualizar el tiempo de la última muestra
    ultima_muestra = tiempo_actual

    # Calcular el ritmo cardíaco en BPM
    if tiempo_entre_latidos != 0:
        ritmo_cardiaco = int(60000 / tiempo_entre_latidos)

    return ritmo_cardiaco


if conectaWifi("FAMILIA ALVIS 2G", "Mapis201"):

    print("Conexión exitosa!")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())

    firebase.setURL("https://cyberdog-cfc41-default-rtdb.firebaseio.com/")
    url = "https://api.thingspeak.com/update?api_key=Z6FGVNL730OY0SU2"

    while True:
        # >>> DHT22 <<<<<
        temperatura, humedad = obtener_temperatura_humedad()
        print("Temperatura: {:.2f} °C, Humedad: {:.2f}%".format(temperatura, humedad))
        sleep_ms(2000)
        message = {"Temperatura °C": temperatura, "% Humedad": humedad}
        firebase.put("cyberdog/sensor_dht22", message, bg=0)
        respuesta = urequests.get(url + "&field1=" + str(temperatura) + "&field2=" + str(humedad))
        print(f"{respuesta.status_code} : Mensaje Enviado dht22")

        # >>> MQ-135 <<<
        valor_gas = obtener_concentracion_gas()
        print("Concentración de gas: {:.2f} %".format(valor_gas))
        sleep_ms(2000)
        message = {"Concentración de gas": valor_gas}
        firebase.put("cyberdog/sensor_mq_135", message, bg=0)
        print("Mensaje Enviado mq135")

        # >>> XD-58C <<<
        ritmo = calcular_ritmo_cardiaco()
        print("Ritmo cardíaco: {} BPM".format(ritmo))
        sleep_ms(1000)  # Esperamos 1 segundo entre cada medición
        message = {"Ritmo cardiaco": ritmo}
        firebase.put("cyberdog/sensor_xd_58c", message, bg=0)
        print("Mensaje Enviado xd-58c")

else:
    print("Imposible conectar al wifi")
    miRed.active(False)
