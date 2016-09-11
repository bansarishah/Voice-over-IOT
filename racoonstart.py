import speech_recognition as sr
import os
import time
import requests

while(True):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            time.sleep(1)
            print("Say something!")
            os.system("say say something")
            audio = r.listen(source)
            print("trying to understand what you just said")
            os.system("say just a sec buddy")
        # Speech recognition using Google Speech Recognition
        try:
            text = r.recognize_google(audio)
            print("You said: " + text)
            os.system(" say you said: " + text)
	    prs = textExtraction(text)
	    print("http://172.16.26.33:5000/racoon?intent="+prs[2]+"&location="+prs[1]+"&action="+prs[0])
            r = requests.get("http://172.16.26.33:5000/racoon?intent="+intent+"&location="+location+"&action="+on_off)
            os.syste,("say " + r.text)
            if(text == "stop"):
                break;
        except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                os.system("say i can not understand what you said, try again")
                #saysomething("Racoon could not understand, try again")
        except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
        except Exception as e:
                print(str(e))
                #saysomething(str(e))

