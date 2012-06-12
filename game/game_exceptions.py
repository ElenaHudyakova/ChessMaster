class InvalidSquareCoordException(Exception):
    def __init__(self, value, coord):
        super(Exception, self).__init__(str(value) + ' for ' + str(coord))

class ImpossibleMoveException(Exception):
    def __init__(self, notation):
        super(Exception, self).__init__(notation)

class InvalidMoveRecordException(Exception):
    def __init__(self, notation):
        super(Exception, self).__init__(notation)

class InvalidBoardSquare(Exception):
    pass

class InvalidGameException(Exception):
    pass

class MoveSavingException(Exception):
    pass

