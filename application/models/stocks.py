"""
DataBase — Stock table
Middle table (NM -> store:product)
"""
from application import db

class Stock(db.Model):
    """Define table & columns"""
    __tablename__ = 'stock'
    id = db.Column(db.Integer, primary_key=True)
    minimum = db.Column(db.Integer)
    stock  = db.Column(db.Integer)
    # foreign key
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    product_sku = db.Column(db.Integer, db.ForeignKey('products.sku'))