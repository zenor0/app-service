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
    
class Issue(db.Model, BaseModel):
    __bind_key__ = 'app'
    __tablename__ = 'issue'
    
    ISSUE_STATE_ENUM = ['pending', 'ongoing', 'closed']
    issue_id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, nullable=False)
    buyer_id = Column(Integer, nullable=False)
    accuser_id = Column(Integer, nullable=False)
    reason = Column(String(256))
    order_id = Column(Integer, nullable=False)
    create_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    JUDGE_RESULT_ENUM = ['seller', 'buyer', 'both', 'none']
    judge_result = Column(Enum(*JUDGE_RESULT_ENUM), default=JUDGE_RESULT_ENUM[3])
    judge_reason = Column(String(256))
    judge_time = Column(DateTime)
    judger_id = Column(Integer)
    state = Column(Enum(*ISSUE_STATE_ENUM), nullable=False, default=ISSUE_STATE_ENUM[0])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def to_dict(self):
        return {
            'issue_id': self.issue_id,
            'seller_id': self.seller_id,
            'buyer_id': self.buyer_id,
            'accuser_id': self.accuser_id,
            'reason': self.reason,
            'order_id': self.order_id,
            'create_time': self.create_time,
            'judge_result': self.judge_result,
            'judge_reason': self.judge_reason,
            'judge_time': self.judge_time,
            'judger_id': self.judger_id,
            'state': self.state,
        }
        

