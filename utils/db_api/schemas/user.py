import os

from sqlalchemy import create_engine, Column, Integer, Boolean, String, Text
from dotenv import load_dotenv
from sqlalchemy.orm import scoped_session, declarative_base, sessionmaker, relationship
from sqlalchemy.schema import ForeignKey

load_dotenv()

host = str(os.getenv("HOST"))
password = str(os.getenv("PASSWORD"))
database = str(os.getenv("DATABASE"))
user = ""

engine = create_engine(f"postgresql+psycopg2://postrges:{password}@{host}/{database}", echo=True)

session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = session.query_property()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, unique=True, primary_key=True, index=True)
    username = Column(String)
    name = Column(String)
    phone = Column(Integer)
    admin = Column(Boolean, default=False)
    topics = relationship("TopicUser", back_populates="user")


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text)
    message = Column(Text(ForeignKey))
    topic_id = Column(Integer, ForeignKey("topic.id", ondelete="CASCADE"), nullable=False)
    topic = relationship("Topic")


class Image(Base):
    __tablename__ = "image"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)


class Topic(Base):
    __tablename__ = "topic"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text, nullable=False)
    messages = relationship("Message")
    # users = relationship("User")
    image_id = Column(Integer, ForeignKey("image.id", ondelete="CASCADE"), nullable=False)
    image = relationship(Image)
    # users_ = relationship("TopicUser", back_populates="topic")


class TopicUser(Base):
    __tablename__ = "topic_user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    topic_id = Column(Integer, ForeignKey("topic.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    role = Column(Text)
    user = relationship(User, back_populates="topics")
    # topic = relationship(Topic, back_populates="users")


session.commit()

Base.metadata.create_all(bind=engine)
