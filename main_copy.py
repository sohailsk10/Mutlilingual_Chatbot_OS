# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import json
from watson_developer_cloud import AssistantV1, LanguageTranslatorV3

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


def main(params):
    # get conversation workspace id
    res = None
    try:
        workspace = '77cdde1e-e030-4f65-9b4e-5ce79b84586f'  # params['assistant_workspace_id']
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
        print('method started')
        print('creating assistant')

        assistant = AssistantV1(
            version='2020-04-01',
            iam_apikey='5WJuZUSBE5w3hdPWp92nGpq_Ia2MkW_xDqOPowm9OEg0',
            url='https://api.eu-de.assistant.watson.cloud.ibm.com/instances/0702f65d-1a2d-4331-ba41-ab31ad9e8fca'
        )

        # response = assistant.message(
        #     workspace_id='77cdde1e-e030-4f65-9b4e-5ce79b84586f',
        #     input={
        #         'text': 'Hi there'
        #     }
        # ).get_result()

        # print('assistant created')
    except exception as e:
        # print(e)
        return {
            'message': 'Please bind your assistant service',
            'context': '{}',
            'output': '{}',
            'intents': '{}',
            'language': ''
        }

    # set up translator
    try:
        translator = LanguageTranslatorV3(
            version='2019-04-03',
            iam_apikey='_8Ls2zNEqP0ulBtGXDcUctoYejpcyKLt32ZdQJScxAZ4',
            url='https://api.eu-gb.language-translator.watson.cloud.ibm.com/instances/88ada459-7f95-4c46-8bac-1963ce3adb57'
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
        text = params['text']
    except:
        text = ''

    # get conversation context if available
    try:
        context = json.loads(params['context'])
    except:
        context = {}

    # detect language
    if text:
        print(text)
        response = translator.identify(text)
        # print(response)
        res = response  # .get_result()
    else:
        res = None
    if res and res['languages'][0]['confidence'] > LT_THRESH:
        language = res['languages'][0]['language']
        print('test', language)
    elif res is None:
        language = BASE_LANGUAGE
    else:
        return {
            'message': 'Sorry, I am not able to detect the language you are speaking. Please try rephrasing.',
            'context': json.dumps(context),
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
            'context': json.dumps(context),
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
        # print('res new',response)
        res = response  # .get_result()
        text = res['translations'][0]['translation']

    # supply language as entity
    text += ' (@language:{})'.format(language)

    # hit conversation
    response = assistant.message(
        workspace_id=workspace,
        input={'text': text},
        context=context
    )
    # print('response new ',response)
    res = response  # .get_result()
    new_context = res['context']
    output = res['output']
    output_text = [text for text in res['output']['text'] if text]
    message = output_text[0]
    output['text'] = output_text
    intents = res['intents']

    # translate back to original language if needed
    if language != BASE_LANGUAGE:
        response = translator.translate(
            output_text,
            source=BASE_LANGUAGE,
            target=language
        )
        res = response  # .get_result()
        output_text = [t['translation'] for t in res['translations']]
        message = output_text[0]
        output['text'] = output_text

    return {
        'message': message,
        'context': json.dumps(new_context),
        'output': json.dumps(output),
        'intents': json.dumps(intents),
        'language': language
    }
