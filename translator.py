# import json
# from ibm_watson import LanguageTranslatorV3, LanguageTranslatorV3
# from watson_developer_cloud import AssistantV1
# from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
#
# authenticator = IAMAuthenticator("XomUspOWjl8V1aFJVidt7cO737uU8weO4DzHEQ-O6Fp2")
# language_translator = LanguageTranslatorV3(
#     version='2018-05-01',
#     authenticator=authenticator
# )
#
# workspace = ('473014ec-a7a6-4ef0-a994-6d89330dba41')
# assistant = AssistantV1(
#     iam_apikey=('Dd0NrWCuy1222pjjGPJ97bPer-NytxAgxOZpXc1EV0xN'),
#     version='2019-03-06'
# )
# translator = LanguageTranslatorV3(
#     version='2019-04-03',
#     iam_apikey='473014ec-a7a6-4ef0-a994-6d89330dba41'
#     # authenticator=authenticator
# )
# language_translator.set_service_url('https://api.eu-gb.language-translator.watson.cloud.ibm.com/instances/9a2d49b6-1b58-4d0c-a5c8-3ea840515d4a')
#
# BASE_LANGUAGE = 'en'
# LT_THRESH = 0.4
# LT_PAIRS = {
#     'ar': 'Arabic',
#     'bg': 'Bulgarian',
#     'zh': 'Chinese (Simplified)',
#     'zht': 'Chinese (Traditional)',
#     'hr': 'Croatian',
#     'cz': 'Czech',
#     'da': 'Danish',
#     'nl': 'Dutch',
#     'et': 'Estonian',
#     'el': 'Greek',
#     'en': 'English',
#     'fi': 'Finnish',
#     'fr': 'French',
#     'de': 'German',
#     'hi': 'Hindi',
#     'he': 'Hebrew',
#     'id': 'Indonesian',
#     'lt': 'Lithuanian',
#     'lv': 'Latvian',
#     'ga': 'Irish',
#     'it': 'Italian',
#     'ja': 'Japanese',
#     'ko': 'Korean',
#     'ms': 'Malay',
#     'nb': 'Norwegian Bokmal',
#     'pl': 'Polish',
#     'pt': 'Portuguese (Brazil)',
#     'ru': 'Russian',
#     'ro': 'Romanian',
#     'es': 'Spanish',
#     'sl': 'Slovenian',
#     'sk': 'Slovak',
#     'sv': 'Swedish',
#     'th': 'Thai',
#     'er': 'Urdu',
#     'vi': 'Vietnamese',
#     'tr': 'Turkish'
# }
#
# text_input = 'Hello, how are you today?'
# if text_input:
#     response = translator.identify(text_input)
#     print("response", response)
#     # print('response', response)
#     res = response  # .get_result()

# translation = language_translator.translate(
#     text=text_input
#     model_id='en-ar').get_result()
# print(json.dumps(translation, indent=2, ensure_ascii=False))
# import pyttsx3
# from gtts import gTTS
# import os
# message = 'سيارة رياضية'
# tts = gTTS(text=message, lang='ar')
# # print(tts)
#
# engine = pyttsx3.init()
# engine.say()
# engine.runAndWait()
#
# print()
#
# tts.save("good.mp3")
# os.system("mpg321 good.mp3")

# from pydub import AudioSegment
# from pydub.playback import play
#
# song = AudioSegment.from_wav("E:\PycharmProjects\multilingual-chatbot\good.mp3")
# play(song)

# from playsound import playsound

# for playing note.wav file
# playsound('good.mp3')
# print('playing sound using  playsound')

# import speech_recognition as sr
#
# # Initialize recognizer class (for recognizing the speech)
#
# r = sr.Recognizer()
#
# # Reading Microphone as source
# # listening the speech and store in audio_text variable
#
# with sr.Microphone() as source:
#     print("Talk")
#     audio_text = r.listen(source)
#     print(audio_text)
#     print("Time over, thanks")
#     # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
#
#     try:
#         # using google speech recognition
#         print("Text: " + r.recognize_google(audio_text))
#     except:
#         print("Sorry, I did not get that")

import speech_recognition as sr

recognizer = sr.Recognizer()

''' recording the sound '''
lang_list = ['ar-KW']

with sr.Microphone() as source:
    print("Adjusting noise ")
    recognizer.adjust_for_ambient_noise(source, duration=1)
    print("Recording for 4 seconds")
    recorded_audio = recognizer.listen(source, timeout=4)
    print("Done recording")

''' Recorgnizing the Audio '''
try:
    print("Recognizing the text")

    text = recognizer.recognize_google(
            recorded_audio,
            language=lang_list
        )
    print("Decoded Text : {}".format(text))

except Exception as ex:
    print(ex)

# import speech_recognition as sr
#
# recognizer = sr.Recognizer()
#
# ''' recording the sound '''
#
# lang = ""
# text_eng = "Friday"
# text_ar = "جمعة"
#
# with sr.Microphone() as source:
#     print("Adjusting noise ")
#     recognizer.adjust_for_ambient_noise(source, duration=1)
#     print("Recording for 4 seconds")
#     recorded_audio = recognizer.listen(source, timeout=4)
#     print(recorded_audio)
#     print("Done recording")
#
# ''' Recorgnizing the Audio '''
# try:
#     print("Recognizing the text")

    # if recorded_audio == text_eng:
    #     text = recognizer.recognize_google(recorded_audio, language='en-US')
    #     print(text)
    # if text == text_eng:
    #     recorded_audio,
    #     language = "en-US"
    #     print("Decoded Text : {}".format(text))

    # elif text == text_ar:
    #     recorded_audio,
    #     language = "ar-KW"
    #     print("Decoded Text : {}".format(text))

# except Exception as ex:
#     print(ex)


