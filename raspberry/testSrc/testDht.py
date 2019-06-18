import Adafruit_DHT

sensor = Adafruit_DHT.DHT11

# GPIO23 (pin no: #16)
pin = 23

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

if humidity is not None and temperature is not None:
    print ("temp = ")
    print (temperature)
    print ("humidity = ")
    print (humidity)
else:
    print ("Failed to get reading.")
