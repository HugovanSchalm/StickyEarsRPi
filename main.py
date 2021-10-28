from flask import Flask, request, jsonify
import threading
import time
import RPi.GPIO as GPIO
import logging

print('Started program')

logging.basicConfig(filename='log.txt', filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)

soundChecked = False
soundDetected = False

def checkSoundLoop():
    global soundChecked, soundDetected
    pinnr = 14
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pinnr, GPIO.IN)
    while True:
        if GPIO.input(pinnr) == 0:
            soundDetected = True
            logging.info("Sound Detected")
        elif soundChecked:
            soundChecked = False
            soundDetected = False
        time.sleep(.001)



app = Flask(__name__)

@app.route('/pair', methods=['POST'])
def pair():
    request_data = request.get_json()
    logging.info("SSID: " + request_data['SSID'] + " | Password: " + request_data['pswd'])
    return jsonify(response="thx")

@app.route('/')
def acknowledge():
    logging.info("Got request at '/'")
    return 'The request works!!!'

@app.route('/checkSound')
def checkSound():
    logging.info("Got request at '/checkSound'")
    global soundDetected, soundChecked
    if soundDetected and not soundChecked:
        soundChecked = True
        return 'yes'
    return 'no'

sound_thread = threading.Thread(target=checkSoundLoop)
sound_thread.start()

app.run(host="0.0.0.0", port=5000, debug=True)

sound_thread.join()
print('Ended program')
