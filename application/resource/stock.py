"""Stock requests"""
# Flask
from flask_restplus import Namespace, Resource, abort, fields, marshal_with
# Models
from application.models import Product, Stock
# Data base
from application import db


# View docs
service = Namespace('stock', description='Stock requests')

stock = service.model('Stock', {
    'id': fields.Integer(read_only=True, description='Product ID'),
    'store_id': fields.Integer(required=True, description='Store ID reference'),
    'product_sku': fields.Integer(required=True, description='SKU number from item'),
    'minimum': fields.Integer(required=True, description='Minimum stock'),
    'stock': fields.Integer(required=True, description='Current stock')
})

# Create settings
stock_parser = service.parser()
stock_parser.add_argument('store_id', type=int, required=True, help='Store ID reference')
stock_parser.add_argument('product_sku', type=int, required=True, help='SKU number from item')
stock_parser.add_argument('minimum', type=int, required=True, help='Minimum stock')
stock_parser.add_argument('stock', type=int, required=True, help='Current stock')


@service.route('/')
class StoreListResource(Resource):
    """
    API to add new stock by item on store
    """

    @service.doc(id='post_stock', parser=stock_parser)
    @service.marshal_with(stock)
    def post(self):
        """Add new stock"""
        args = stock_parser.parse_args()
        stock = db.session.query(Stock).filter(
            Stock.store_id==args['store_id'], 
            Stock.product_sku==args['product_sku']
        ).first()
        if stock:
            abort(404, message=f'The product is already registered in this store')
        
        stock = Stock(store_id = args['store_id'],
            product_sku = args['product_sku'],
            minimum = args['minimum'],
            stock = args['stock']
        )
        db.session.add(stock)
        db.session.commit()
        
        return stock, 201