
class FluxonError(Exception):
    def __init__(self, message = "An error occurred"):
        self.message = message

    def __str__(self):
        return self.message


class UnRecognizedInputFormatError(FluxonError):
    def __init__(self, message = "Unrecognized input format"):
        self.message = message

    def __str__(self):
        return self.message
    


class MalformedJsonError(FluxonError):
    def __init__(self, message = "Malformed JSON detected"):
        self.message = message

    def __str__(self):
        return self.message
    

class UnExpectedCharacterError(FluxonError):
    def __init__(self, message = "Unexpected character"):
        self.message = message

    def __str__(self):
        return self.message