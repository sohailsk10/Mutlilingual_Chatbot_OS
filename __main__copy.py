import json
from watson_developer_cloud import AssistantV1, LanguageTranslatorV3
# from ibm_watson import AssistantV1, LanguageTranslatorV3
from src.conversation import Conversation

# consts
BASE_LANGUAGE = 'en'
LT_THRESH = 0.4
LT_PAIRS = {
    'ar': 'Arabic',
    'bg': 'Bulgarian',
    'zh': 'Chinese (Simplified)',
    'zht': 'Chinese (Traditional)',
    'hr': 'Croatian',
    'cz': 'Czech',
    'da': 'Danish',
    'nl': 'Dutch',
    'et': 'Estonian',
    'el': 'Greek',
    'en': 'English',
    'fi': 'Finnish',
    'fr': 'French',
    'de': 'German',
    'hi': 'Hindi',
    'he': 'Hebrew',
    'id': 'Indonesian',
    'lt': 'Lithuanian',
    'lv': 'Latvian',
    'ga': 'Irish',
    'it': 'Italian',
    'ja': 'Japanese',
    'ko': 'Korean',
    'ms': 'Malay',
    'nb': 'Norwegian Bokmal',
    'pl': 'Polish',
    'pt': 'Portuguese (Brazil)',
    'ru': 'Russian',
    'ro': 'Romanian',
    'es': 'Spanish',
    'sl': 'Slovenian',
    'sk': 'Slovak',
    'sv': 'Swedish',
    'th': 'Thai',
    'er': 'Urdu',
    'vi': 'Vietnamese',
    'tr': 'Turkish'
}


def main():
    # get conversation workspace id
    try:
        # print("Workspace")
        # workspace = params['assistant_workspace_id']
        workspace = "473014ec-a7a6-4ef0-a994-6d89330dba41"
        # print("workspace", workspace)
    except:
        return {
            'message': 'Please bind your assistant workspace ID as parameter',
            'context': '{}',
            'output': '{}',
            'intents': '{}',
            'language': ''
        }

    # set up conversation
    try:
        # print("Assistant")
        assistant = AssistantV1(
            # iam_apikey=params['assistant_apikey'],
            iam_apikey="Dd0NrWCuy1222pjjGPJ97bPer-NytxAgxOZpXc1EV0xN",
            version='2019-03-06'
        )
    except:
        return {
            'message': 'Please bind your assistant service',
            'context': '{}',
            'output': '{}',
            'intents': '{}',
            'language': ''
        }

    # set up translator
    try:
        # print("Translator start")
        # authenticator = IAMAuthenticator(params['translator_apikey'])
        translator = LanguageTranslatorV3(
            version='2019-04-03',
            # iam_apikey=params['translator_apikey']
            iam_apikey="ut5yA-d4A73QZGth02NUwB7nyYwFDq8hupd8pZXrU1ET"
            # authenticator=authenticator
        )
        # print("Translator end")
    except:
        return {
            'message': 'Please bind your language translator service',
            'context': '{}',
            'output': '{}',
            'intents': '{}',
            'language': ''
        }

    # check for empty or null string
    context = {}
    while True:
        try:
            # print("Text")
            # text = params['text']
            text = input("type a text: ")
            # print('text ', text)
        except:
            text = ''

        # get conversation context if available
        # try:
        #     # print("Context")
        #     context = json.loads( params['context'] )
        #     print('context: ', context)
        # except:

        # if context != None:
        #     pass

        # detect language
        if text:
            response = translator.identify(text)
            # print('response', response)
            res = response.get_result()
            # print('res', res)
            # print("response", response)
        else:
            res = None

        # print(res['languages'][0])
        if res and res['languages'][0]['confidence'] > LT_THRESH:
            language = res['languages'][0]['language']
        elif res is None:
            language = BASE_LANGUAGE
        else:
            print('message Sorry, I am not able to detect the language you are speaking. Please try rephrasing.'),
            context = context,
            output = '{}',
            intents = '{}',
            language = ''
        # print('language',language)
        # validate support for language
        if language not in LT_PAIRS.keys():
            print('message: Sorry, I do not know how to translate between {} and {} yet.'.format(BASE_LANGUAGE, language))
            context = context
            output = '{}'
            intents = '{}'
            language = language

        # translate to base language if needed
        # try:
        if language != BASE_LANGUAGE:
            response = translator.translate(
                text,
                source=language,
                target=BASE_LANGUAGE
            )
            # print('res new',response)
            res = response.get_result()
            text = res['translations'][0]['translation']
            print(text)
        # supply language as entity
        text += ' (@language:{})'.format( language )
        # print("text", text)
        # print(context)
        # print('translate if', text)
        # hit conversation
        response = assistant.message(
            workspace_id=workspace,
            input={'text': text},
            context=context
        )
        # print('response_final: ', response)
        res = response.get_result()
        new_res = response.get_result()
        # print(res)
        # print("RES:", res)
        new_context = res['context']
        output = res['output']
        output_text = [text for text in res['output']['text'] if text]
        message = output_text[0]
        # print(message)
        output['text'] = output_text
        # print(output['text'])
        intents = res['intents']
        # print(intents)

        # translate back to original language if needed
        if language != BASE_LANGUAGE:
            response = translator.translate(
                output_text,
                source=BASE_LANGUAGE,
                target=language
            )
            res = response.get_result()
            output_text = [t['translation'] for t in res['translations']]
            message = output_text[0]
            # print("Message", message)
            output['text'] = output_text
            # print("Output_Text", output['text'])
        print(message)
        # print(language)

        context = new_res['context']
        # else:
        # message = message

        # def converse(self):
        #     msg = input(self.lastOutput + '\n')
        #     # print("MSG", msg)
        #     res = self.makeRequest(msg, self.lastContext)
        #     print("res", res)
        #     self.lastContext = res['context']
        #     self.lastOutput = res['message']
        # return {
        #     'message': message,
        #     'context': json.dumps( new_context ),
        #     'output': json.dumps( output ),
        #     'intents': json.dumps( intents ),
        #     'language': language,
        # }
        # return context

main()


