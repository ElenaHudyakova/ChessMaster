class InvalidMoveException(Exception):
    def __init__(self, message):
        super(InvalidMoveException, self).__init__(message)


class InvalidCaptureException(Exception):
    def __init__(self, message):
        super(InvalidCaptureException, self).__init__(message)

class InvalidMoveRecord(Exception):
    def __init__(self, message):
        super(InvalidMoveRecord, self).__init__(message)