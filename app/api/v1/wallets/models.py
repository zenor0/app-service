from app import db
from datetime import datetime
from sqlalchemy import *
# from sqlalchemy.orm import synonym

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

class Wallet(db.Model, BaseModel):
    __bind_key__ = 'app'
    __tablename__ = 'wallet'
    
    WALLET_STATES_ENUM = ['normal', 'locked']
    wallet_id = Column('uid', Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, unique=True)
    balance = Column(DECIMAL(10, 2))
    state = Column(Enum(*WALLET_STATES_ENUM), nullable=False, default=WALLET_STATES_ENUM[0])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def to_dict(self):
        return {
            'uid': self.wallet_id,
            'user_id': self.user_id,
            'state': self.state,
            'balance': self.balance,
            }
        

