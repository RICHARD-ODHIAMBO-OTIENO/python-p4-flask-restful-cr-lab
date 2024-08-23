from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Plant(db.Model, SerializerMixin):
    __tablename__ = 'plants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)   # Adding the name column
    image = db.Column(db.String, nullable=False)  # Adding the image column
    price = db.Column(db.Numeric(10, 2), nullable=False)  # Adding the price column