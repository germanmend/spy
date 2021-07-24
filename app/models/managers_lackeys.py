from app import db
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin


class ManagerLackey(db.Model, SerializerMixin):
    __tablename__ = 'managers_lackeys'

    manager_id = db.Column(db.Integer,
                           db.ForeignKey('hitmen.id'),
                           primary_key=True,
                           nullable=False)
    lackey_id = db.Column(db.Integer,
                           db.ForeignKey('hitmen.id'),
                           primary_key=True,
                           nullable=False)

    manager = relationship('Hitman', foreign_keys=[manager_id])
    lackeys = relationship('Hitman', foreign_keys=[lackey_id])
