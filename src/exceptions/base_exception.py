class BaseException(Exception):
    def __init__(self, *args, status_code:int = 400):
        super().__init__(*args)
        self.status_code = status_code