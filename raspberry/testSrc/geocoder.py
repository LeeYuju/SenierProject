import geocoder
latlng = geocoder.ip('me').latlng
print(latlng)
print(latlng[0])
print(latlng[1])
