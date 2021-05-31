# # from watson_developer_cloud import AssistantV1, LanguageTranslatorV3
# # import speech_recognition as sr
# # import pyttsx3
# #
# # BASE_LANGUAGE = 'en'
# # LT_THRESH = 0.4
# # LT_PAIRS = {
# #     'ar': 'Arabic',
# #     'bg': 'Bulgarian',
# #     'zh': 'Chinese (Simplified)',
# #     'zht': 'Chinese (Traditional)',
# #     'hr': 'Croatian',
# #     'cz': 'Czech',
# #     'da': 'Danish',
# #     'nl': 'Dutch',
# #     'et': 'Estonian',
# #     'el': 'Greek',
# #     'en': 'English',
# #     'fi': 'Finnish',
# #     'fr': 'French',
# #     'de': 'German',
# #     'hi': 'Hindi',
# #     'he': 'Hebrew',
# #     'id': 'Indonesian',
# #     'lt': 'Lithuanian',
# #     'lv': 'Latvian',
# #     'ga': 'Irish',
# #     'it': 'Italian',
# #     'ja': 'Japanese',
# #     'ko': 'Korean',
# #     'ms': 'Malay',
# #     'nb': 'Norwegian Bokmal',
# #     'pl': 'Polish',
# #     'pt': 'Portuguese (Brazil)',
# #     'ru': 'Russian',
# #     'ro': 'Romanian',
# #     'es': 'Spanish',
# #     'sl': 'Slovenian',
# #     'sk': 'Slovak',
# #     'sv': 'Swedish',
# #     'th': 'Thai',
# #     'er': 'Urdu',
# #     'vi': 'Vietnamese',
# #     'tr': 'Turkish'
# # }
# #
# # workspace_id = "473014ec-a7a6-4ef0-a994-6d89330dba41"
# # assistant_api_key = "Dd0NrWCuy1222pjjGPJ97bPer-NytxAgxOZpXc1EV0xN"
# # translator_api_key = "ut5yA-d4A73QZGth02NUwB7nyYwFDq8hupd8pZXrU1ET"
# #
# # r = sr.Recognizer()
# #
# # def main(command):
# #     # get conversation workspace id
# #     try:
# #         workspace = workspace_id
# #     except:
# #         return {
# #             'message': 'Please bind your assistant workspace ID as parameter',
# #             'context': '{}',
# #             'output': '{}',
# #             'intents': '{}',
# #             'language': ''
# #         }
# #
# #     # set up conversation
# #     try:
# #         assistant = AssistantV1(
# #             iam_apikey=assistant_api_key,
# #             version='2019-03-06'
# #         )
# #     except:
# #         return {
# #             'message': 'Please bind your assistant service',
# #             'context': '{}',
# #             'output': '{}',
# #             'intents': '{}',
# #             'language': ''
# #         }
# #
# #     try:
# #         translator = LanguageTranslatorV3(
# #             version='2019-04-03',
# #             iam_apikey=translator_api_key
# #         )
# #     except:
# #         return {
# #             'message': 'Please bind your language translator service',
# #             'context': '{}',
# #             'output': '{}',
# #             'intents': '{}',
# #             'language': ''
# #         }
# #
# #     context = {}
# #     while True:
# #         try:
# #             text = input("Input Text: ")
# #         except:
# #             text = ''
# #
# #         engine = pyttsx3.init()
# #         engine.say(command)
# #         engine.runAndWait()
# #
# # while (1):
# #     try:
# #         translator = LanguageTranslatorV3(
# #             version='2019-04-03',
# #             iam_apikey=translator_api_key
# #         )
# #     except:
# #         print("Please bind your language translator service")
# #         # return {
# #         #     'message': 'Please bind your language translator service',
# #         #     'context': '{}',
# #         #     'output': '{}',
# #         #     'intents': '{}',
# #         #     'language': ''
# #         # }
# #
# #     try:
# #         with sr.Microphone() as source2:
# #             r.adjust_for_ambient_noise(source2, duration=0.5)
# #             print("Start recordng")
# #
# #             audio2 = r.listen(source2)
# #
# #             MyText = r.recognize_google(audio2)
# #             MyText = MyText.lower()
# #
# #             print("SPEECH_INPUT " + MyText)
# #             if MyText:
# #                 response = translator.identify(MyText)
# #                 res = response.get_result()
# #             else:
# #                 res = None
# #
# #             main(MyText)
# #
# #     except sr.RequestError as e:
# #         print("Could not request results; {0}".format(e))
# #
# #     except sr.UnknownValueError:
# #         print("unknown error occured")
#
# import json
# from ibm_watson import SpeechToTextV1
# from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
#
# authenticator = IAMAuthenticator('Hl1j5EveT13lvOfQEJXtlzhh4iO40hP1ka4HXXgRWd3c')
# speech_to_text = SpeechToTextV1(
#     authenticator=authenticator
# )
#
# speech_to_text.set_service_url('https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/05832848-e165-4349-94af-40fec4b8c9d4')
#
# speech_models = speech_to_text.list_models().get_result()
# print(json.dumps(speech_models, indent=2))




#


import json
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator('Dd0NrWCuy1222pjjGPJ97bPer-NytxAgxOZpXc1EV0xN')
assistant = AssistantV2(
    version='2020-04-01',
    authenticator = authenticator
)

assistant.set_service_url('https://api.us-south.assistant.watson.cloud.ibm.com/instances/7cd79f59-361f-4408-ad9c-962be8aa6c2f')

response=assistant.bulk_classify(
    skill_id='473014ec-a7a6-4ef0-a994-6d89330dba41',
    input=[{'text': 'friday'}]).get_result()

# responese = assistant.bulk_classify(skill_id='473014ec-a7a6-4ef0-a994-6d89330dba41',input=[""]).get_result()

print(json.dumps(response, indent=2))