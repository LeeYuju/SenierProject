import requests

deviceId = "123"
dust = "20"

url = "http://101.101.164.197/insert_dust_data.php"
url += "?deviceId="
url += deviceId
url += "&dust="
url += dust

r = requests.get(url)

print(r.status_code)
print(r.headers)
print(r.content)
