from sqlalchemy import Column, Integer, String

from alchemy import Base, engine


class Models(Base):
    __tablename__ = 'md'

    page = Column(Integer)
    image = Column(String)
    date = Column(String)
    currency = Column(String)
    price = Column(String)


Base.metadata.create_all(engine)
