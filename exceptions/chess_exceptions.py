class InvalidMoveException(Exception):
    def __init__(self, message):
        Exception.__init__(message)


class InvalidCaptureException(Exception):
    def __init__(self, message):
        Exception.__init__(message)