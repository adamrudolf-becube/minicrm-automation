class Expectation:
    def __init__(self, expected_request, response, repeatedly = False):
        self.request = expected_request
        self.response = response
        self.repeatedly = repeatedly
