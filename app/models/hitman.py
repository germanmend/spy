from alembic import op
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

from app import db


class Hitman(db.Model, SerializerMixin):
    __tablename__ = 'hitmen'

    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String(100),
                     index=False,
                     unique=False,
                     nullable=False)
    email = db.Column(db.String(100),
                      index=True,
                      unique=True,
                      nullable=False)
    is_active = db.Column(db.Boolean,
                          index=False,
                          unique=False,
                          nullable=False,
                          default=True,
                          server_default='True')
    level = db.Column(db.Text,
                      index=False,
                      unique=False,
                      nullable=True)
    created_at = db.Column(db.DateTime,
                           index=False,
                           unique=False,
                           nullable=False,
                           default=str(datetime.utcnow()),
                           server_default=str(datetime.utcnow()))
