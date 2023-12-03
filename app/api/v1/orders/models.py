from app import db
from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import synonym



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

class Order(db.Model, BaseModel):
    __bind_key__ = 'app'
    __tablename__ = 'order'
    
    ORDER_STATE_ENUM = ['pending', 'paid', 'delivered', 'completed', 'canceled', 'refunded', 'locked', 'closed']
    order_id = Column('uid', Integer, primary_key=True)
    from_id = Column(Integer, nullable=False)
    to_id = Column(Integer, nullable=False)
    good_id = Column(Integer, nullable=False)
    state = Column(Enum(*ORDER_STATE_ENUM), nullable=False, default=ORDER_STATE_ENUM[0])
    price = Column(DECIMAL(10, 2))
    create_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    pay_time = Column(DateTime)
    complete_time = Column(DateTime)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def to_dict(self):
        return {
            'uid': self.order_id,
            'from_id': self.from_id,
            'to_id': self.to_id,
            'good_id': self.good_id,
            'state': self.state,
            'price': self.price,
            'create_time': datetime.isoformat(self.create_time, sep=' '),
            'pay_time': datetime.isoformat(self.pay_time, sep=' '),
            'complete_time': self.complete_time
            }
        

