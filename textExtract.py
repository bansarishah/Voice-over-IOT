import sys
from wit import Wit
import requests
#import speech_recognition as sr
#import os
#import time

def textExtraction(text):
	def send(request, response):
	    print(response['text'])

	def turn_on(request):
	    context = request['context']
	    entities = request['entities']
	    context['turn'] = 'on'
	    return context

	actions = {
	    'send': send, 
	    'turnOn': turn_on,
	}

	client = Wit(access_token = 'access_token', actions=actions)
	resp = client.message(text)
	print(resp)
	temp_map = dict()
	temp_map.clear()
	entities = resp['entities']
	intent = entities['intent'][0]['value']
	if (entities.get('temperature')):
		temperature = str(entities['temperature'][0]['value'])
		print(intent, temperature)
		temp_map['intent'] = intent
		temp_map['location'] = "bedroom"
		temp_map['temperature'] = temperature
		#print("http://172.16.26.33:5000/racoon3?intent="+intent+"&temperature="+str(temperature))
		#requests.get("http://172.16.26.33:5000/racoon3?intent="+intent+"&temperature="+str(temperature))
	else :
		location = entities['location'][0]['value']
		on_off = resp['entities']['on_off'][0]['value']
		if (entities.get('question')) :
			question = resp['entities']['question'][0]['value']
			print(intent, location ,on_off, question)
			temp_map['intent'] = intent
			temp_map['location'] = location
			temp_map['action'] = on_off
			temp_map['question'] = question
			print("http://172.16.26.33:5000/racoon2?intent="+intent+"&location="+location+"&action="+on_off+"&question="+question)
			#r=requests.get("http://172.16.26.33:5000/racoon2?intent="+intent+"&location="+location+"&action="+on_off+"&question="+question)
			#print(r.text)
		else :
			print(intent, location ,on_off)
			temp_map['location'] = location
			temp_map['intent'] = intent
			temp_map['action'] = on_off
			print("http://172.16.26.33:5000/racoon?intent="+intent+"&location="+location+"&action="+on_off)
			#r = requests.get("http://172.16.26.33:5000/racoon?intent="+intent+"&location="+location+"&action="+on_off)
			#print(r.text)
	return (temp_map)

# while(True):
#	r = sr.Recognizer()
#	with sr.Microphone() as source:
#	    time.sleep(1)
#	    print("Say something!")
#	    os.system("say say something")
#	    audio = r.listen(source)
#	    print("trying to understand what you just said")
#	    os.system("say just a sec buddy")
#	# Speech recognition using Google Speech Recognition
#	try:
#	    text = r.recognize_google(audio)
#	    print("You said: " + text)
#	    os.system(" say you said: " + text)
#	    os.system("say " + textExtraction(text))
#	    if(text.lower() == "stop"):
#	    	break;
#	except sr.UnknownValueError:
#		print("Google Speech Recognition could not understand audio")
#		os.system("say i can not understand what you said, try again")
#		#saysomething("Racoon could not understand, try again")
#	except sr.RequestError as e:
#		print("Could not request results from Google Speech Recognition service; {0}".format(e))
#	except Exception as e:
#		print(str(e))
#		#saysomething(str(e))


# client = Wit(access_token=access_token, actions=actions)
# client.interactive()

# resp = client.message('Switch on Bedroom light')

# on_off = resp['entities']['on_off'][0]['value']
# location = resp['entities']['location'][0]['value']
# intent = resp['entities']['intent'][0]['value']

# print(on_off,location,intent)

