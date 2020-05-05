from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'img-processing-svc'

@app.route('/api/v1/processed')
def processing():
    return {
        'at': '20230215T124231Z',
        'type': 'DETECTED_RESULT',
        'detected_plate': '34ABC123',
    };

    app.run()