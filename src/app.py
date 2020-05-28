import re
import traceback

from flask import Flask
app = Flask(__name__)
from detector.plateDetector import PlateDetector
from datetime import datetime

@app.route('/health')
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

@app.route('/api/v1/detected/plates')
def processing():
    try:
        date_iso = datetime.now().isoformat()
        detector = PlateDetector()
        plate_text = detector.detect('./test/resources/test2.jpg')
        match = re.search('([0-9]{2} [A-Z]{1,4} [0-9]{1,3})', plate_text)
        return {
            'at': date_iso,
            'result': ('success' if match else 'fail'),
            'detected_plate': match.group(1),
        };
    except Exception as e:
        return {
            'at': date_iso,
            'result': 'fail',
            'cause': traceback.format_exc()
        }
app.run()