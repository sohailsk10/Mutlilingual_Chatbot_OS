import json
from watson_developer_cloud import LanguageTranslatorV3
from watson_developer_cloud import AssistantV2

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




def main( params ):


    # get conversation workspace id
    print("PARAMS__", params)
    # try:
    #     print("Workspace")
    #     workspace = params['assistant_workspace_id']
    #     # print("workspace", workspace)
    # except:
    #     return {
    #         'message': 'Please bind your assistant workspace ID as parameter',
    #         'context': '{}',
    #         'output': '{}',
    #         'intents': '{}',
    #         'language': ''
    #     }

    # set up conversation
    try:
        # print("Assistant")
        # assistant = AssistantV1(
        #     iam_apikey=params['assistant_apikey'],
        #     version='2019-03-06'
        # )
        assistant_api = params['assistant_apikey']
        # authenticator = IAMAuthenticator(assistant_api)

        assistant = AssistantV2(
            version='2018-09-20',
            iam_apikey=assistant_api,
            url='https://api.eu-gb.assistant.watson.cloud.ibm.com/instances/76fa3d44-f247-4a0b-a826-ff47eb98a891'
            # authenticator=authenticator
        )
        Assistant_Api = params['assistant_id']
        assistant.create_session(Assistant_Api)
        # assistant.set_service_url(
        #     'https://api.eu-gb.assistant.watson.cloud.ibm.com/instances/76fa3d44-f247-4a0b-a826-ff47eb98a891')
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
        print("Translator start")

        translator_api = params['translator_apikey']
        translator = LanguageTranslatorV3(
            version='2018-05-01',
            iam_apikey=translator_api,
            url='https://api.us-south.language-translator.watson.cloud.ibm.com/instances/5e8a8531-a1d8-493d-86db-a27a82d1ffbf'
        )
    except:
        return {
            'message': 'Please bind your language translator service',
            'context': '{}',
            'output': '{}',
            'intents': '{}',
            'language': ''
        }

    # check for empty or null string
    try:
        if params['text'] != None:
            text = params['text']
            print('param text',text)
        elif params['_ow_headers'] != None:
            val = params['_ow_headers']
            text = val['text']
            print('header value text', text)

    except:
        text = ''

    # get conversation context if available
    try:
        print("Context")
        context = json.loads( params['context'] )
    except:
        context = {}

    # detect language
    if text:
        response = translator.identify(text)
        res = response.get_result()
    else:
        res = None
    if res and res['languages'][0]['confidence'] > LT_THRESH:
        language = res['languages'][0]['language']
    elif res is None:
        language = BASE_LANGUAGE
    else:
        return {
            'message': 'Sorry, I am not able to detect the language you are speaking. Please try rephrasing.',
            'context': json.dumps( context ),
            'output': '{}',
            'intents': '{}',
            'language': ''
        }
    # validate support for language
    if language not in LT_PAIRS.keys():
        return {
            'message': 'Sorry, I do not know how to translate between {} and {} yet.'.format(
                BASE_LANGUAGE, language
            ),
            'context': json.dumps( context ),
            'output': '{}',
            'intents': '{}',
            'language': language
        }
    # translate to base language if needed
    if language != BASE_LANGUAGE:
        response = translator.translate(
            text,
            source=language,
            target=BASE_LANGUAGE
        )
        res = response.get_result()
        text = res['translations'][0]['translation']

    # supply language as entity
    text += ' (@language:{})'.format( language )

    # hit conversation
    Session_ID = assistant.create_session(Assistant_Api)

    sess_id = Session_ID.get_result()['session_id']
    print("SESSION_ID", sess_id)

    response = assistant.message(
        assistant_id=Assistant_Api,
        session_id=sess_id,
        input={'text': text},
        context=context
    )
    # print('response_final: ', response)
    # res = response.get_result()
    # print("RES--->:", res)
    # new_context = res['context']
    # output = res['output']
    # output_text = [text for text in res['output']['text'] if text]
    # message = output_text[0]
    # # print(message)
    # output['text'] = output_text
    # print(output['text'])
    # intents = res['intents']
    # # print(intents)
    #
    # # translate back to original language if needed
    # if language != BASE_LANGUAGE:
    #     response = translator.translate(
    #         output_text,
    #         source=BASE_LANGUAGE,
    #         target=language
    #     )
    #     res = response.get_result()
    #     output_text = [t['translation'] for t in res['translations']]
    #     message = output_text[0]
    #     print("Message", message)
    #     output['text'] = output_text
        # print("Output_Text", output['text'])

    res = response
    new_res = res.get_result()
    def_context = new_res
    new_context = new_res['output']['generic'][0]['text']

    output = new_context
    # output_text = output
    Output_TEXT = output

    message = output
    # print("MESSAGE", message)
    # output['text'] = output_text
    # # intents = res['intents']
    # print(intents)

    # translate back to original language if needed
    if language != BASE_LANGUAGE:
        response = translator.translate(
            Output_TEXT,
            source=BASE_LANGUAGE,
            target=language
        )
        res = response.get_result()
        for t in res['translations']:
            Output_TEXT = t['translation']
        message = Output_TEXT


    return {
        'message': message,
        'session': sess_id,
        # 'context': json.dumps( new_context ),
        # 'output': json.dumps( output ),
        # 'intents': json.dumps( intents ),
        # 'type': type_text,
        'language': language,
    }
