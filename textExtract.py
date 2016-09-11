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

	client = Wit(access_token="25HHBAQ44RFUK4JNZHLK2WMGKGLNCXKE", actions=actions)
	resp = client.message(text)

	on_off = resp['entities']['on_off'][0]['value']
	location = resp['entities']['location'][0]['value']
	intent = resp['entities']['intent'][0]['value']

	print(on_off,location,intent)
	temp_map = dict()
	temp_map['action'] = on_off
	temp_map['location'] = location
	temp_map['intent'] = intent
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

