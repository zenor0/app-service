from app import db
from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import synonym, DeclarativeBase
import re

from hashlib import md5

EMAIL_REGEX = re.compile(r"^\S+@\S+\.\S+$")
USERNAME_REGEX = re.compile(r"^\S+$")

def check_length(attribute, length):
    """Checks the attribute's length."""
    try:
        return bool(attribute) and len(attribute) <= length
    except:
        return False


class BaseModel:
    """Base for all models, providing save, delete and from_dict methods."""

    def __commit(self):
        """Commits the current db.session, does rollback on failure."""
        from sqlalchemy.exc import IntegrityError

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def delete(self):
        """Deletes this model from the db (through db.session)"""
        db.session.delete(self)
        self.__commit()

    def save(self):
        """Adds this model to the db (through db.session)"""
        db.session.add(self)
        self.__commit()
        return self

    @classmethod
    def from_dict(cls, model_dict):
        return cls(**model_dict).save()

import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

def hash_and_salt_password(plain_password):
    salt =  os.environ.get("SALT")
    return md5((plain_password + salt).encode('utf-8')).hexdigest()

def check_password_hash(plain_password, hashed_password):
    return hash_and_salt_password(plain_password) == hashed_password


class User(db.Model, BaseModel):
    __bind_key__ = 'app'
    __tablename__ = 'user'
    
    user_id = Column('uid', Integer, primary_key=True)
    _username = Column("username", db.String(64), unique=True)
    _email = Column("email", db.String(64), unique=True)
    _password = Column('password', String(256))
    nickname = Column(String(40))
    realname = Column(String(40))
    id_number = Column(String(20))
    register_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    blocked = Column(Boolean, nullable=False, default=False)
    profile = ''
    
    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        is_valid_length = check_length(username, 64)
        if not is_valid_length or not bool(USERNAME_REGEX.match(username)):
            raise ValueError(f"{username} is not a valid username")
        self._username = username

    username = synonym("_username", descriptor=username)
    
    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        if not check_length(email, 64) or not bool(EMAIL_REGEX.match(email)):
            raise ValueError(f"{email} is not a valid email address")
        self._email = email

    email = synonym("_email", descriptor=email)

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        if not bool(password):
            raise ValueError("no password given")

        hashed_password = hash_and_salt_password(password)
        if not check_length(hashed_password, 128):
            raise ValueError("not a valid password, hash is too long")
        self._password = hashed_password

    password = synonym("_password", descriptor=password)
    
    def verify_password(self, password):
        return check_password_hash(self._password, password)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def to_dict(self):
        return {
            'uid': self.user_id,
            'username': self.username,
            'nickname': self.nickname,
            'realname': self.realname,
            'id_number': self.id_number,
            'profile': '',
            'email': self.email,
            'blocked': self.blocked,
            'register_time': datetime.isoformat(self.register_time, sep=' ')
            }
        

