#Declare libraries
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    category_name = Column(String(100), nullable=False)
    url = Column(String(200), nullable=False)

    def __repr__(self):
        return "<Article(title='%s', description = '%s', category = '%s',url = '%s' )>" \
               % (self.title, self.description,self.category,self.url)

engine = create_engine('mysql://root:1234@localhost/phase2', echo=True)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
