import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

SQLAlchemyBase = declarative_base()

class Feedback(SQLAlchemyBase):
    __tablename__ = "feedback"

    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, nullable=False)
    fault_id = sa.Column(sa.String, nullable=False)
    car_brand = sa.Column(sa.String, nullable=True)
    car_model = sa.Column(sa.String, nullable=True)
    was_helpful = sa.Column(sa.Boolean, nullable=True)
    symptom_accurate = sa.Column(sa.Boolean, nullable=True)
    comment = sa.Column(sa.String, nullable=True)
    created_at = sa.Column(sa.DateTime, default=sa.func.now())
