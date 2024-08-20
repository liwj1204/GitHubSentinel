from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class RepoUpdate(Base):
    __tablename__ = 'repo_updates'
    id = Column(Integer, primary_key=True)
    repo_url = Column(String)
    update_time = Column(DateTime, default=datetime.datetime.utcnow)
    update_content = Column(String)

class DatabaseClient:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def connect(self):
        Base.metadata.create_all(self.engine)

    def store_update(self, repo_url, update_content):
        session = self.Session()
        new_update = RepoUpdate(repo_url=repo_url, update_content=update_content)
        session.add(new_update)
        session.commit()
        session.close()

    def retrieve_updates(self, repo_url=None):
        session = self.Session()
        if repo_url:
            updates = session.query(RepoUpdate).filter_by(repo_url=repo_url).all()
        else:
            updates = session.query(RepoUpdate).all()
        session.close()
        return updates
