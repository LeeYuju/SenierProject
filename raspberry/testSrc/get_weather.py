from pyowm import OWM
import geocoder

latlng = geocoder.ip('me').latlng

owm = OWM('4cef2e1e7c19f03b36ed971bac0be5fc')
obs = owm.weather_at_coords(latlng[0], latlng[1])
print(latlng[0])
print(latlng[1])

location = obs.get_location()

print(location.get_name())

w = obs.get_weather()
print(w.get_status())
print(w.get_temperature(unit='celsius')['temp'])
print(w.get_humidity())
print(w.get_wind()['speed'])

text = "현재 날씨는 "

#w.get_temperature(unit='celsius')['temp']
