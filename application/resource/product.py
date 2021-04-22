"""Product requests"""
# Flask
from flask_restplus import Namespace, Resource, abort, fields, marshal_with
# Models
from application.models import Product, Stock
# Data base
from application import db


# View docs
service = Namespace('product', description='Product requests')

product = service.model('Product', {
    'sku': fields.Integer(required=False, description='Product ID'),
    'product': fields.String(required=True, description='Product name')
})
stock = service.model('Stock', {
    'id': fields.Integer(read_only=True, description='Stock ID'),
    'store_id': fields.Integer(required=True, description='Store ID reference'),
    'product_sku': fields.Integer(required=True, description='SKU number from product'),
    'minimum': fields.Integer(required=True, description='Minimum stock'),
    'stock': fields.Integer(required=True, description='Current stock')
})

# Create settings
product_parser = service.parser()
product_parser.add_argument('sku', type=int, required=False, help='Product ID')
product_parser.add_argument('product', type=str, required=True, help='Product name')

# Update settings
update_product_parser = service.parser()
update_product_parser.add_argument('product', type=str, required=True, help='Product name')



@service.route('/')
class ProductsResource(Resource):
    """
    Display all product records.
    Allow to create new item
    """

    @service.doc(id='get_products')
    @service.marshal_with(product)
    def get(self):
        """Display all products records"""
        products = db.session.query(Product).all() 
        return products
    
    @service.doc(id='post_product', parser=product_parser)
    @service.marshal_with(product)
    def post(self):
        """Add new item"""
        args = product_parser.parse_args()
        product = Product(product=args['product'])
        
        if args['sku']:
            if db.session.query(Product).filter(Product.sku==args['sku']):
                product.sku = args['sku']
            else:
                abort(404, message=f'SKU already exists:{args["sku"]}')
        
        db.session.add(product)
        db.session.commit()
        
        return product, 201


@service.route('/<sku>')
class ProductResource(Resource):
    """
    Display a product by SKU,
    Allow Edit OR delete by SKU
    """

    @service.doc(id='get_product')
    @service.marshal_with(product)
    def get(self, sku):
        """Retuns first item by SKU"""
        product = db.session.query(Product).filter(Product.sku == sku).first()
        if not product:
            abort(404, message=f'SKU not found:{sku}')
        return product
    
    @service.doc(id='update_product', parser=update_product_parser)
    @service.marshal_with(product)
    def patch(self, sku):
        """Update records"""
        args = update_product_parser.parse_args()
        product = db.session.query(Product).filter(Product.sku == sku).first()
        if not product:
            abort(404, message=f'SKU not found:{sku}')
        product.product = args['product']
        
        db.session.add(product)
        db.session.commit()
        
        return product, 201

    @service.doc(id='delete_product')
    def delete(self, sku):
        """Delete an item"""
        product = db.session.query(Product).filter(Product.sku == sku).first()
        if not product:
            abort(404, message=f'SKU not found:{sku}')
        
        db.session.delete(product)
        db.session.commit()
        
        return {}, 204


@service.route('/<sku>/tiendas/')
class ProductInStockResource(Resource):
    """
    Shows a list of all stores with stock
    """
    @service.doc(id='get_stores_with_stock')
    @service.marshal_with(stock)
    def get(self, sku):
        """List the stores where there is stock by SKU"""
        stock = db.session.query(Stock).filter(Stock.product_sku == sku, Stock.stock >= 1).all()
        if not stock:
            abort(404, message=f'There is no stock of the product {sku} in any store')
        return stock