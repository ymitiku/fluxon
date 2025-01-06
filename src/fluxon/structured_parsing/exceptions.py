
class FluxonError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class UnRecognizedInputFormatError(FluxonError):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
    


class MalformedJsonError(FluxonError):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
    

class UnExpectedCharacterError(FluxonError):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message