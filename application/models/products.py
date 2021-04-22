"""DataBase — Products table"""
from application import db

class Product(db.Model):
    """Define table & columns"""
    __tablename__ = 'products'
    sku = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(255))
    # use on foreign key
    stocks = db.relationship('Stock', backref='product', lazy=True)