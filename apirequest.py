class ApiRequest:
    def __init__(self, url, method, slogan, payload={}):
        self.url = url
        self.method = method
        self.slogan = slogan
        self.payload = payload
