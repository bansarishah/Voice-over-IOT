import sys
from wit import Wit
import requests
import speech_recognition as sr


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

	print("http://172.16.26.33:5000/racoon?intent="+intent+"&location="+location+"&action="+on_off)	
	requests.get("http://172.16.26.33:5000/racoon?intent="+intent+"&location="+location+"&action="+on_off)	


# text = input("Please enter your command: ")
# textExtraction(text)

while(True):
	r = sr.Recognizer()
	with sr.Microphone() as source:
	    print("Say something!")
	    # speech.say("say something")
	    audio = r.listen(source)
	    print("heard something.., lemme check ")
	    # speech.say("heard something")
	# Speech recognition using Google Speech Recognition
	try:
	    text = r.recognize_google(audio)
	    print("You said: " + text)
	    # speech.say("you said: " + text)
	    textExtraction(text)
	    if(text.lower() == "bye"):
	    	break;
	except sr.UnknownValueError:
		print("Google Speech Recognition could not understand audio")
	#	speech.say("Racoon could not understand, try again")
	except sr.RequestError as e:
		print("Could not request results from Google Speech Recognition service; {0}".format(e))
	except Exception as e:
		print(str(e))
	#	speech.say(str(e))



# client = Wit(access_token=access_token, actions=actions)
# client.interactive()

# resp = client.message('Switch on Bedroom light')

# on_off = resp['entities']['on_off'][0]['value']
# location = resp['entities']['location'][0]['value']
# intent = resp['entities']['intent'][0]['value']

# print(on_off,location,intent)

