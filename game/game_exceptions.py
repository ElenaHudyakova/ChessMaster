class InvalidSquareCoordException(Exception):
    def __init__(self, value, coord):
        super(Exception, self).__init__(str(value) + ' for ' + str(coord))

class ImpossibleMoveException(Exception):
    pass

class InvalidMoveRecordException(Exception):
    pass

class InvalidBoardSquare(Exception):
    pass

class InvalidGameException(Exception):
    pass

class MoveSavingException(Exception):
    pass

