class TextAnalyser(object):

    @staticmethod
    def actions_from_text(text):
        print("Speech: {}".format(text))
        return "Server: ({})".format(text)