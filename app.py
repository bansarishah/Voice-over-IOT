from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import time
from textExtract import textExtraction
GPIO.setmode(GPIO.BOARD)

GPIO.setup(36, GPIO.OUT)
GPIO.setup(40, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)

app = Flask(__name__)
map = dict()

map['bedroomlight'] = 36
map['kitchenlight'] = 40
map['bathroomlight'] = 37
map['bedroomac'] = 33
@app.route('/')
def index():
    return render_template('index.html', bathlight = get_status(map['bathroomlight']), bedroomlight = get_status(map['bedroomlight']), kitchenlight = get_status(map['kitchenlight']), message = "")

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
def do_the_job2():
    action = request.args.get("action")
    intent = request.args.get("intent")
    location = request.args.get("location")
    do_gpio_job(action, map[location+intent])
    return " Switching " + action + " " + location + " " + intent 

@app.route('/racoon2', methods = ['GET'])
def do_the_job():
    action = request.args.get("action")
    intent = request.args.get("intent")
    location = request.args.get("location")
    question = request.args.get("question")
    return question_status(location, intent, action)

@app.route('/racoon3', methods = ['GET'])
def do_the_job3():
    temp = request.args.get("temperature")
    intent = request.args.get("intent")
    location = "bedroom"
    # set temp
    return "the A.C. temperature is set to " + temp 

def question_status(location, intent, action):
    temp = dict()
    temp[1] = "on"
    temp[0] = "off"
    status = temp[get_status(map[location+intent])]
    if(status == action ):
        return "Yes, the " + location + " " + intent + " is " + action
    else:
        return "No, the " + location + " " + intent + " is " + status
    
@app.route('/process', methods = ['GET'])
def process_text():
    msg = "Please try again."
    mode = "web"
    try:
        text = request.args.get("text")
        mode = request.args.get("mode")
        prs = textExtraction(text)
        print(prs)
        if("temperature" in prs):
            msg = "The A.C temperature is set to " + prs['temperature']
        elif('question' in prs):
            msg = question_status(prs['location'], prs['intent'], prs['action'])
        else:
            do_gpio_job(prs['action'],map[prs['location'] + prs['intent']])
            msg = "Switched " + prs['action'] + " " + prs['location'] + "  " + prs['intent']
        
        if(mode == "app"):
            print("mode app returning " + msg )
            return msg
        print("mode not app returning" + msg)
        return render_template('index.html', bathlight = get_status(map['bathroomlight']), bedroomlight = get_status(map['bedroomlight']), kitchenlight = get_status(map['kitchenlight']), message = msg )
    except Exception as e:
	print("error " +str(e))
    if(mode == "app"):
        print("returning default msg mode app")
        return msg
    print("retrunng defalutl msg, mode not app")
    return render_template('index.html', bathlight = get_status(map['bathroomlight']), bedroomlight = get_status(map['bedroomlight']), kitchenlight = get_status(map['kitchenlight']), message = msg )

def do_gpio_job(action, pin):
    if(action == "on"):
        GPIO.output(pin, True)
    else:
        GPIO.output(pin, False)
    return

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
