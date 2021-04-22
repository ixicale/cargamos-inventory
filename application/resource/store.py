"""Store requests"""
# Flask
from flask_restplus import Namespace, Resource, abort, fields, marshal_with
# Models
from application.models import Store, Stock
# Data base
from application import db


# View docs
service = Namespace('store', description='Store requests')

store = service.model('Store', {
    'id': fields.Integer(read_only=True, description='Store ID'),
    'store': fields.String(required=True, description='Store name'),
    'address': fields.String(required=True, description='Store address')
})
stock = service.model('Stock', {
    'id': fields.Integer(read_only=True, description='Stock ID'),
    'store_id': fields.Integer(required=True, description='Store ID reference'),
    'product_sku': fields.Integer(required=True, description='SKU number from product'),
    'minimum': fields.Integer(required=True, description='Minimum stock'),
    'stock': fields.Integer(required=True, description='Current stock')
})

# Create settings
store_parser = service.parser()
store_parser.add_argument('store', type=str, required=True, help='Store name')
store_parser.add_argument('address', type=str, required=True, help='Store address')

stock_parser = service.parser()
stock_parser.add_argument('product_sku', type=int, required=True, help='SKU number product')
stock_parser.add_argument('minimum', type=int, required=True, help='Minimum stock')
stock_parser.add_argument('stock', type=int, required=True, help='Current stock')

# Update settings
update_store_parser = service.parser()
update_store_parser.add_argument('store', type=str, required=False, help='Store name')
update_store_parser.add_argument('address', type=str, required=False, help='Store address')

update_stock_parser = service.parser()
update_stock_parser.add_argument('minimum', type=int, required=False, help='Minimum stock')
update_stock_parser.add_argument('stock', type=int, required=False, help='Current stock')

@service.route('/')
class StoreListResource(Resource):
    """
    Display all product records.
    Allow to create new records
    """

    @service.doc(id='get_stores')
    @service.marshal_with(store)
    def get(self):
        """Display all store records"""
        stores = db.session.query(Store).all()
        return stores
    
    @service.doc(id='post_store', parser=store_parser)
    @service.marshal_with(store)
    def post(self):
        """Add new store"""
        args = store_parser.parse_args()
        store = Store(store=args['store'], address=args['address'])
        
        db.session.add(store)
        db.session.commit()
        
        return store, 201


@service.route('/<id>')
class StoreResource(Resource):
    """
    Display a store by ID,
    Allow Edit OR delete by ID
    """
    @service.doc(id='get_store')
    @service.marshal_with(store)
    def get(self, id):
        """Retuns first item by ID"""
        store = db.session.query(Store).filter(Store.id == id).first()
        if not store:
            abort(404, message=f'Store ID not found:{id}')
        return store
    
    @service.doc(id='update_store', parser=update_store_parser)
    @service.marshal_with(store)
    def patch(self, id):
        """Update records"""
        args = update_store_parser.parse_args()
        store = db.session.query(Store).filter(Store.id == id).first()
        if not store:
            abort(404, message=f'Store ID not found:{id}')

        if parsed_args['store']:
            store.store = parsed_args['store']
        if parsed_args['address']:
            store.address = parsed_args['address']
        
        db.session.add(store)
        db.session.commit()
        
        return store, 201

    @service.doc(id='delete_store')
    def delete(self, id):
        """Delete record"""
        store = db.session.query(Store).filter(Store.id == id).first()
        if not store:
            abort(404, message=f'Store ID not found:{id}')
        
        db.session.delete(store)
        db.session.commit()
        
        return {}, 204


@service.route('/<id>/stock')
class StoreListResource(Resource):
    """
    List all stock by ID store.
    Allows you to enter new products
    """

    @service.doc(id='get_stock')
    @service.marshal_with(stock)
    def get(self, id):
        """List store stocks"""
        stock = db.session.query(Stock).filter(Stock.store_id == id).all()
        if not stock:
            abort(404, message=f'No items were found in the store id: {id}')
        return stock
    
    @service.doc(id='post_stock', parser=stock_parser)
    @service.marshal_with(stock)
    def post(self, id):
        """Add new product on store"""
        args = stock_parser.parse_args()
        stock = db.session.query(Stock).filter(
            Stock.store_id==int(id), 
            Stock.product_sku==args['product_sku']
        ).first()
        if stock:
            abort(404, message=f'Products already exists on this Store id:{id}')
        stock = Stock(store_id = int(id),
            product_sku = args['product_sku'],
            minimum = args['minimum'],
            stock = args['stock']
        )
        db.session.add(stock)
        db.session.commit()
        
        return stock, 201


@service.route('/<id>/stock/insufficient')
class insufficientStockResource(Resource):
    """
    Displays a list of all stock where it is less than the minimum
    """

    @service.doc(id='get_insufficient_stock')
    @service.marshal_with(stock)
    def get(self, id):
        """Returns the list of insufficient product stocks list by store"""
        stock = db.session.query(Stock).filter(Stock.store_id == id, Stock.stock <= Stock.minimum).all()
        if not stock:
            abort(404, message=f'There is insufficient stock in the store with id:{id}')
        return stock
    

@service.route('/<id>/stock/<sku>')
class UpdateStockResource(Resource):
    """
    Allows you to update store stocks
    """

    @service.doc(id='update_stock', parser=update_stock_parser)
    @service.marshal_with(stock)
    def patch(self, id, sku):
        """Update stock by store ID"""
        parsed_args = update_store_parser.parse_args()
        stock = db.session.query(Stock).filter(
            Stock.store_id==int(id), 
            Stock.product_sku==int(sku)
        ).first()
        if not stock:
            abort(404, message=f'There is no stock of the product {sku} in the store {id}')
        
        if parsed_args['minimum'] != None:
            stock.minimum = parsed_args['minimum']
        if parsed_args['stock'] != None:
            stock.stock = parsed_args['stock']

        db.session.add(stock)
        db.session.commit()

        return stock, 201