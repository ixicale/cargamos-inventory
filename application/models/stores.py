"""DataBase — Store table"""
from application import db

class Store(db.Model):
    """Define table & columns"""
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    store = db.Column(db.String(255))
    address = db.Column(db.String(255))
    # use on foreign key
    stocks = db.relationship('Stock', backref='store', lazy=True)
