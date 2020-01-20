"""database models."""

import sqlalchemy
import psycopg2

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, PickleType, BigInteger, Unicode
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Tweet(Base):

    __tablename__ = 'tweets'

    id = Column(BigInteger, primary_key=True)
    text = Column(Unicode(500), nullable=False)
    sentiment = Column(Integer, nullable=False)

    def __repr__(self):
        return f'<tweet {self.text}>'