from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

from app import db


class Hit(db.Model, SerializerMixin):
    __tablename__ = 'hits'

    id = db.Column(db.Integer,
                   primary_key=True)
    description = db.Column(db.String(100),
                            index=False,
                            unique=False,
                            nullable=False)
    target = db.Column(db.String(100),
                       index=False,
                       unique=False,
                       nullable=False)
    hitman_id = db.Column(db.Integer,
                          db.ForeignKey('hitmen.id'),
                          nullable=True)
    assigned_by_id = db.Column(db.Integer,
                               db.ForeignKey('hitmen.id'),
                               nullable=True)
    status = db.Column(db.String(50),
                       index=False,
                       unique=False,
                       nullable=True,
                       default='active',
                       server_default='active')
    is_active = db.Column(db.Boolean,
                          index=False,
                          unique=False,
                          nullable=False,
                          server_default='False')
    created_at = db.Column(db.DateTime,
                           index=False,
                           unique=False,
                           nullable=False,
                           default=str(datetime.utcnow()),
                           server_default=str(datetime.utcnow()))

    hitman = relationship('Hitman', foreign_keys=[hitman_id])
    assigned_by = relationship('Hitman', foreign_keys=[assigned_by_id])
