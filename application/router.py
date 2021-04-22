"""Requests"""
# Flask begins
from flask_restplus import Api
# resources/namespaces
from .resource import *


api = Api(
    title='Inventory manage — ixicale',
    version='1.0', 
    description='Cargamos — API TEST'
)

api.add_namespace(product)
api.add_namespace(store)
api.add_namespace(stock)