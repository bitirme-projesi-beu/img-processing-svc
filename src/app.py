import re
import traceback
import requests
import os
import json

from threading import Thread
from flask import Flask
from detector.plateDetector import PlateDetector
from datetime import datetime
from time import sleep
from dotenv import load_dotenv, find_dotenv

server = Flask(__name__)
load_dotenv(find_dotenv())

test_data_paths = ['test1.jpg', 'test2.jpg', 'test3.jpg']

@server.route('/health', methods=['GET'])
def index():
    try:
        detector = PlateDetector()
        return {
            'status': 'up',
            'at': datetime.now().today()
        }
    except:
        return {
            'status': 'down',
            'at': datetime.now().isoformat()
        }

@server.route('/api/v1/detected/test', methods=['GET'])
def processing():
    try:
        date_iso = datetime.now().isoformat()
        detector = PlateDetector()
        plate_text = detector.detect('./test/resources/test1.jpg')
        return {
            'at': date_iso,
            'result': 'success',
            'detected_plate': plate_text,
        };
    except Exception as e:
        return {
            'at': date_iso,
            'result': 'fail',
            'cause': traceback.format_exc()
        }

@server.route('/api/v1/detection/start', methods=['GET'])
def start():
    start_process.start()
    date_iso = datetime.now().isoformat()
    return {
        'result': 'Detection started.',
        'at': date_iso
    }

def start_detection():
    try:
        detector = PlateDetector()
        domain = os.getenv("BACKEND_SERVICE_URL")
        TOKEN = os.getenv("HARD_TOKEN")
        RESOURCE_PATH = os.getenv("RESOURCE_PATH")
        URL = f"{domain}/api/v2/tickets"

        for image_path in test_data_paths:
            sleep(15)
            detection_result = detector.detect(f"{RESOURCE_PATH}/{image_path}")
            detection_result = os.linesep.join([s for s in detection_result.splitlines() if s and len(s) > 1])
            detection_result = detection_result.replace(" ", "")
            date_iso = datetime.now().isoformat()
            data = {
                "parkingLotId": 7,
                "plate": detection_result,
                "createdAt": date_iso
            }
            headers = {"content-type": "application/json", "authorization": "Bearer "+ TOKEN}
            res = requests.post(URL, data=json.dumps(data), headers=headers)
            print('Res', res.content)
            print(detection_result)
    except Exception as e:
            print('Exception', e)

if __name__ == "__main__":
    start_process = Thread(target=start_detection)
    server.run(debug=True)
    # create in memory db
    pass
