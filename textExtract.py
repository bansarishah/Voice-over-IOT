import sys
from wit import Wit
import requests

def textExtraction(text):
	if len(sys.argv) != 2:
	    print('usage: python ' + sys.argv[0] + ' <wit-token>')
	    exit(1)
	access_token = sys.argv[1]

	# Quickstart example
	# See https://wit.ai/ar7hur/Quickstart

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

	client = Wit(access_token=access_token, actions=actions)
	resp = client.message(text)

	on_off = resp['entities']['on_off'][0]['value']
	location = resp['entities']['location'][0]['value']
	intent = resp['entities']['intent'][0]['value']

	print(on_off,location,intent)

	print("http://172.16.26.33:5000/racoon?intent="+intent+"&location="+location+"&action="+on_off)	
	requests.get("http://172.16.26.33:5000/racoon?intent="+intent+"&location="+location+"&action="+on_off)	


text = input("Please enter your command: ")
textExtraction(text)



# client = Wit(access_token=access_token, actions=actions)
# client.interactive()

# resp = client.message('Switch on Bedroom light')

# on_off = resp['entities']['on_off'][0]['value']
# location = resp['entities']['location'][0]['value']
# intent = resp['entities']['intent'][0]['value']

# print(on_off,location,intent)

