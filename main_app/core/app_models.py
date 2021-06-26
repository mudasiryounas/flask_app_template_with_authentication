

class BaseResponse:
    def __init__(self, is_success=True, message='OK', response_code=200, data=None):
        self.is_success = is_success
        self.message = message
        self.exception = None
        self.response_code = response_code
        self.data = data

    def fail(self, response_code=500, message='Sorry! An unexpected error has occurred, Please reload the page and try again.'):
        self.response_code = response_code
        self.message = message
        self.is_success = False
