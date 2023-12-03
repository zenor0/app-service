from app import db
from datetime import datetime
# import enum
from sqlalchemy import *
from sqlalchemy.orm import synonym
from hashlib import md5

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
    # print(plain_password, hashed_password)
    return hash_and_salt_password(plain_password) == hashed_password

    
class AdminUser(db.Model, BaseModel):
    __tablename__ = 'admin_user'
    
    ADMINUSER_LEVEL_ENUM = ['superuser', 'admin']
    admin_id = Column(Integer, nullable=True, primary_key=True, unique=True)
    username = Column(String(20), nullable=False, unique=True)
    _password = Column('password', String(128), nullable=False)
    level = Column(Enum(*ADMINUSER_LEVEL_ENUM), nullable=False, default=ADMINUSER_LEVEL_ENUM[1])
    create_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    
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
        return check_password_hash(password, self._password)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def to_dict(self):
        return {
            'admin_id': self.admin_id,
            'username': self.username,
            'level': self.level,
            'create_time': datetime.isoformat(self.create_time, ' ')
            }
