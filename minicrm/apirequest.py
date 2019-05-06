GET_METHOD = "GET"
PUT_METHOD = "PUT"


class ApiRequest:
    def __init__(self, url, method, slogan, payload={}):
        self._url = url
        if method != GET_METHOD and method != PUT_METHOD:
            raise ValueError("Unsupported method type: {}".format(method))
        else:
            self._method = method
        self._slogan = slogan
        self._payload = payload

    def get_url(self):
        return self._url

    def get_method(self):
        return self._method

    def get_slogan(self):
        return self._slogan

    def get_payload(self):
        return self._payload
