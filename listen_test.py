import speech_recognition as sr 
recognizer = sr.Recognizer()

# with sr.Microphone() as source:
#     print("Jarvis:Listening....")
#     # audio = recognizer.listen(source)
#     recognizer.pause_threshold = 2.0 
#     audio = recognizer.listen(
#         source,
#         timeout=10,
#         phrase_time_limit=30
#     )
#     print("Jarvis:processing your voice..")
recognizer.pause_threshold =2.0
def listen():
    try:
        with sr.Microphone() as source:
            print("Jarvis:Adjusting background noise..") 

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            print("Jarvis:Listening....")
            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=30
            )
        print("Jarvis:processing...")    

        text = recognizer.recognize_google(
            audio,
            language="en-IN"

        )
        return text 
    
                  
# try:
#     text =  recognizer.recognize_google(audio)
#     print("YOu said:",text)
    except sr.WaitTimeoutError:
         print("Jarvis:you did not say anything.") 
         return None
    except sr.UnknownValueError:
        print("Jarvis: Sorry, I Could not understand you.")
        return None    
    except sr.RequestError :
        print("Jarvis: Speech recognition service is unavailable.")
        return None
    except OSError as error:
        print("Jarvis: Microphone error",error)
        return None
user_input =listen()
if user_input:
    print("You said:",user_input)
else:
    print("Jarvis: no valid input received.")    