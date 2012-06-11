from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

engine = create_engine('mysql+mysqldb://root:123@localhost:3306/chess', echo=True)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)

session = Session()

