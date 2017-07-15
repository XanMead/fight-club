from sqlalchemy import create_engine
from models import Base

DB_NAME = 'stack.db'

engine = create_engine("sqlite:///%s" % DB_NAME)

Base.metadata.create_all(engine)