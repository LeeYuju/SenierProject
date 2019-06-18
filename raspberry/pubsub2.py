# -*- coding: utf-8 -*-
#for tts
from __future__ import print_function
import time
import paho.mqtt.client as paho
import board
import neopixel
import threading
import json
import RPi.GPIO as GPIO
import serial
from pyowm import OWM
import geocoder
import requests

#for tts
import grpc
import gigagenieRPC_pb2
import gigagenieRPC_pb2_grpc
import MicrophoneStream as MS
import user_auth as UA
import os
from ctypes import *
HOST = 'gate.gigagenie.ai'
PORT = 4080
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
  dummy_var = 0
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
asound = cdll.LoadLibrary('libasound.so')
asound.snd_lib_error_set_handler(c_error_handler)

# TTS : getText2VoiceStream
def getText2VoiceStream(inText,inFileName):
	channel = grpc.secure_channel('{}:{}'.format(HOST, PORT), UA.getCredentials())
	stub = gigagenieRPC_pb2_grpc.GigagenieStub(channel)
	message = gigagenieRPC_pb2.reqText()
	message.lang=0
	message.mode=0
	message.text=inText
	writeFile=open(inFileName,'wb')
	for response in stub.getText2VoiceStream(message):
		if response.HasField("resOptions"):
			print ("\n\nResVoiceResult: %d" %(response.resOptions.resultCd))
		if response.HasField("audioContent"):
			print ("Audio Stream\n\n")
			writeFile.write(response.audioContent)
	writeFile.close()
	return response.resOptions.resultCd


#아두이노와 통신 포트 확보
port = "/dev/ttyUSB0"
serialFromArduino = serial.Serial(port, 9600)
serialFromArduino.flushInput()

#mqtt 브로커 및 토픽정의
broker="101.101.164.197"
pubTopic = "moodlight/onTopic/"
subTopic = "moodlight/inTopic/"

#해당 디바이스의 아이디!!
deviceId = "123"

#네오픽셀 핀 및 초기화
pixel_pin = board.D12
pixels = neopixel.NeoPixel(pixel_pin, 12, brightness=0.2, auto_write=False, pixel_order=neopixel.GRB)

# mqtt 메세지 수신시 실행되는 콜백함수
def on_message(client, userdata, message):
    time.sleep(1)
    print("received message =",str(message.payload.decode("utf-8")))
    str_m = str(message.payload.decode("utf-8"))
    if len(str_m) < 2:
        actWeatherData()
        return
    dict = json.loads(str(message.payload.decode("utf-8")))
    actNeoPixel(dict['r'],dict['g'],dict['b'])

# 네오픽셀 rgb led수행
def actNeoPixel(r, g, b):
    print("act pixel")
    pixels.fill((r, g, b))
    pixels.show()

# 아두이노에서 받은 센서 데이터를 서버로 전송
def publishSensorData(input):
    client.publish(pubTopic + deviceId, input)
    if "{" in str(input):
        dict = json.loads(str(input))
        sendDustAlarm(dict['dust'])

# 미세먼지 수치가 일정 수준 이상인 경우 서버로 푸시알람 요청
def sendDustAlarm(dust):
    print("json dust : ")
    print(dust)
    if dust >= 0.5: #미세먼지 경고 수준 100
        url = "http://101.101.164.197/insert_dust_data.php"
        url += "?deviceId="
        url += deviceId
        url += "&dust="
        url += str(dust)
        r = requests.get(url)


# 날씨 나타내기 신호 수신 시 작동
def actWeatherData():
    print("actWeather")
    output_file = "test.wav"
    getText2VoiceStream(getWeatherData(), output_file)
    MS.play_file(output_file)
    print( output_file + "이 생성되었으니 파일을 확인바랍니다. \n\n\n")

# 현 위치의 날씨정보 받아내기
def getWeatherData():
    #네트워크 상 현 위치 추적
    geo = geocoder.ip('me')
    latlng = geo.latlng
    state = geo.state
    print(state)
    # open weather map api활용 -> 분당 60회 콜 무료
    owm = OWM('4cef2e1e7c19f03b36ed971bac0be5fc')
    obs = owm.weather_at_coords(latlng[0], latlng[1])
    location = obs.get_location()
    print(location.get_name())
    w = obs.get_weather()
    print(w.get_status())
    result = "현재 날씨는 " + getWeatherStatus(str(w.get_status())) + "입니다."
    result += ("기온은" + str(w.get_temperature(unit='celsius')['temp']) + ", ")
    result += "습도는" + str(w.get_humidity()) + "이며 "
    result += "풍속은" + str(w.get_wind()['speed']) + "입니다."
    neopixelTemp(w.get_temperature(unit='celsius')['temp'])
    print(result)
    return result

def getWeatherStatus(status):
    if status in "Thunderstorm":
        return "천둥"
    elif status in "Drizzle":
        return "이슬비"
    elif status in "Rain":
        return "비"
    elif status in "Snow":
        return "눈"
    elif status in "Mist":
        return "안개"
    elif status in "Smoke":
        return "연기"
    elif status in "Haze":
        return "연무"
    elif status in "Dust":
        return "미세먼지"
    elif status in "Fog":
        return "안개"
    elif status in "Sand":
        return "황사"
    elif status in "Ash":
        return "재"
    elif status in "Squall":
        return "태풍"
    elif status in "Cloud":
        return "흐림"
    else:
        return "맑음"

def neopixelTemp(temp):
    if temp >= 20:
        actNeoPixel(0,0,255)
    else:
        actNeoPixel(0,255,0);

# mqtt 연결 및 구독
client= paho.Client("client-001")
client.on_message=on_message
print("connecting to broker ",broker)
client.connect(broker)
client.loop_start()
print("subscribing ")
client.subscribe(subTopic + deviceId)
time.sleep(2)
print("publishing start")

while(True):
    # 아두이노로 부터 센서데이터 수신 시
    if(serialFromArduino.inWaiting() > 0):
        input = serialFromArduino.readline().decode("utf-8")
        print(input)
        publishSensorData(input)

#client.disconnect() #disconnect
#client.loop_stop() #stop loop
