from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import time
from textExtract import textExtraction
GPIO.setmode(GPIO.BOARD)

GPIO.setup(36, GPIO.OUT)
GPIO.setup(40, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)

app = Flask(__name__)
map = dict()

map['bedroom'] = 36
map['kitchen'] = 40
map['bathroom'] = 37

@app.route('/')
def index():
    return render_template('index.html', bathlight = get_status(map['bathroom']), bedroomlight = get_status(map['bedroom']), kitchenlight = get_status(map['kitchen']), message = "")

def get_status(pin):
    return GPIO.input(pin);

# @app.route('/map_port', methods = ['POST'])
# def mapPort():
#     global map
#     loc = request.form("location")
#     port = request.form("port")
#     if( loc in map):
#         return "already exists"
#     else:
#         map[loc] = port
#         print(map)
#         return ("adding " + port + "for " + loc) 

@app.route('/racoon', methods = ['GET'])
def do_the_job():
    action = request.args.get("action")
    intent = request.args.get("intent")
    location = request.args.get("location")
    do_gpio_job(action, map[location])
    return " Switching " + action + " " + location + " " + intent
    
@app.route('/process', methods = ['GET'])
def process_text():
    text = request.args.get("text")
    prs = textExtraction(text)
    do_gpio_job(prs[0],map[prs[1]])
    return render_template('index.html', bathlight = get_status(map['bathroom']), bedroomlight = get_status(map['bedroom']), kitchenlight = get_status(map['kitchen']), message = text)

def do_gpio_job(action, pin):
    if(action == "on"):
        GPIO.output(pin, True)
    else:
        GPIO.output(pin, False)
    return

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
