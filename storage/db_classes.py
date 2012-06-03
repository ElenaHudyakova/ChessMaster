from sqlalchemy import Column, Integer, String
from sqlalchemy.schema import ForeignKey
from sqlalchemy.types import BIGINT
from storage.db_connection import Base

class GameDB(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, autoincrement=True)
    event = Column(String)
    date = Column(String)
    site = Column(String)
    result = Column(String)
    white = Column(String)
    black = Column(String)
    round = Column(String)

class MoveDB(Base):
    __tablename__ = 'moves'

    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    notation = Column(String)
    number = Column(Integer)
    color = Column(Integer)
    serial1 = Column(BIGINT)
    serial2 = Column(BIGINT)
    serial3 = Column(BIGINT)
    serial0 = Column(BIGINT)