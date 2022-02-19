# sudo python lego-lights.py
import board
import busio
import digitalio
import adafruit_tlc5947
from time import sleep

from flask import Flask, render_template, Response, request, redirect, url_for, jsonify

DRIVER_COUNT = 2
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI)
latch = digitalio.DigitalInOut(board.D5)
tlc5947 = adafruit_tlc5947.TLC5947(spi, latch, num_drivers=DRIVER_COUNT)

delay = 0.5

range_count = DRIVER_COUNT * 24
index = 24
# for i in range(48):
#	  tlc5947[i] = 4095

sleep(5)

for i in range(48):
	tlc5947[i] = 0

while False:
	tlc5947[index] = 4095
	sleep(delay)
	tlc5947[index] = 0
	index+=1
	if index == 32:
		index = 24

brightness = 0
while False:
	tlc5947[24] = brightness
	sleep(0.2)
	brightness+=50
	if brightness > 4095:
		brightness = 0


# web
app = Flask(__name__)

@app.route('/')

def index():
    return render_template('index.html')

@app.route("/control", methods=['GET', 'POST'])
def control():
  if request.method == 'GET':
    arr = [0 for x in range(range_count)]
    for i in range(range_count):
      print(i)
      arr[i] = tlc5947[i]
    print(arr)
    return jsonify(arr)

  content = request.json
  print(content)
  value = 0
  if content['task'] == 'on':
    value = 4095
  index = content['index']
  if index == -1:
    for i in range(range_count):
      tlc5947[i] = value
  else:
    tlc5947[index] = value
  return jsonify({'task': content['task'] + ' done'}), 201

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')

