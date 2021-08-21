import asyncio
from bleak import BleakClient
import unicodedata
import time
import requests
import json
import pygatt

adapter = pygatt.GATTToolBackend()
BLE_ADDRESS_ARDUINO = "3E:2A:44:72:2D:C2"
BLE_ADDRESS ="00:60:37:0a:ac:f5"

spo2 = "19b10001-e8f2-537e-4f6c-d104768a1214"

#async def run (addres):
#	async with BleakClient(BLE_ADDRESS_ARDUINO) as client:
#		data_spo2 = await client.read_gatt_char(spo2)
#		print("SP02: {0}".format(int.from_bytes(data_spo2,byteorder = 'little',signed=False)))
#loop = asyncio.get_event_loop()
#loop.run_until_complete(run(BLE_ADDRESS_ARDUINO))
SENSOR_UUIDS={
	"air_quality_co2" : "08d41e61-ac11-40a2-a95a-e0e0fb5336fa"
}


sensor_values = {}

try:
	adapter.start()
	divice = adapter.connect(BLE_ADDRESS)
	while True:
		async def run (addres):
			async with BleakClient(BLE_ADDRESS_ARDUINO) as client:
				data_spo2 = await client.read_gatt_char(spo2)
				data_push_spo2 =(int.from_bytes(data_spo2,byteorder='little',signed=False))
				print(data_push_spo2)
		loop = asyncio.get_event_loop()
		loop.run_until_complete(run(BLE_ADDRESS_ARDUINO))
	#while True:
		for sensor, uuid in SENSOR_UUIDS.items():
			initial = divice.char_read(uuid)
			value = initial.decode('utf-8').rstrip('\x00')
			sensor_values[sensor] = float(value)
		print(sensor_values['air_quality_co2'])
		data_push_oksigen = '\r\n{\r\n "m2m:cin": {\r\n "cnf": "message",\r\n "con": "\r\n {\r\n \t \\"Oksigen\\": \\"'+str(sensor_values['air_quality_co2'])+'\\",\r\n \\"Satuan\\": \\"O2\\"}\r\n "\r\n}\r\n}'
		url = 'https://platform.antares.id:8443/~/antares-cse/antares-id/Smart-Home-Tecorp/oksigen'
		headers = {'cache-control':'no-cache','content-type':'application/json;ty=4','x-m2m-origin':'1508d89ba90b3afe:4b3b5d3738ec34e3'}
		requests.post(url,headers=headers,data=data_push_oksigen)
		time.sleep(10)
finally:
	adapter.stop()
	#loop.run_until_complete(run(BLE_ADDRESS_ARDUINO))
