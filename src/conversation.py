# wrapper around cloud function for multilingual chatbot


import requests


class Conversation:
    def __init__( self, host=None, namespace=None, package=None, action=None ):
        self.host = host
        self.namespace = namespace
        self.package = package
        self.action = action
        self.lastContext = {}
        self.lastOutput = 'Type here to begin the conversation:'
        self.base = 'https://{}/api/v1/web'.format( self.host )

    # hit multilingual chatbot cloud function service and return response
    def makeRequest( self, msg, context ):
        body = {
            'text': msg,
            'context': context
        }
        print(self.base)
        print(self.namespace)
        print(self.package)
        print(self.action)
        response = requests.post(
            '{}/{}/{}/{}.json'.format(
                self.base,
                self.namespace,
                self.package,
                self.action
            ),
            data=body
        )
        print()
        print(response)
        return response.json()

    # print response and wait for user input
    def converse( self ):
        msg = input( self.lastOutput + '\n' )
        # print("MSG", msg)
        res = self.makeRequest( msg, self.lastContext)
        print("res", res)
        self.lastContext = res['context']
        self.lastOutput = res['message']
