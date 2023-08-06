from . import session

class LewdsAPI(object):

    def __init__(self, ctx):
        self.name = ctx

    def nsfw(self):
        path = 'https://lewds.fun/api/v1/nsfw/{}'.format(self)
        response = session.get(path)

        if response.json()["error"] == True:
            return ("Invalid API Key Provided!")

        if response.json()["error"] == "False": 
           return response.json()['result']