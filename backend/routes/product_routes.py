from flask import Blueprint, request, jsonify
from models.product import Product
from models import db
from models.order_detail import OrderDetail
from models.purchase_order_detail import PurchaseOrderDetail
from models.product_vendor import ProductVendor

product_bp = Blueprint('product_routes', __name__, url_prefix='/api/products')

@product_bp.route('/', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        "ProductID": product.ProductID,
        "ProductName": product.ProductName,
        "ProductCode": product.ProductCode,
        "UnitPrice": str(product.UnitPrice),
        "QuantityPerUnit": product.QuantityPerUnit
    } for product in products])

@product_bp.route('/<int:ProductID>', methods=['GET'])
def get_product(ProductID):
    product = Product.query.get_or_404(ProductID)
    return jsonify(product.to_dict())

@product_bp.route('/', methods=['POST'])
def create_product():
    data = request.json
    new_product = Product(
        ProductName=data['ProductName'],
        ProductCode=data['ProductCode'],
        UnitPrice=data['UnitPrice'],
        QuantityPerUnit=data['QuantityPerUnit']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201

@product_bp.route('/<int:ProductID>', methods=['PUT'])
def update_product(ProductID):
    product = Product.query.get_or_404(ProductID)
    data = request.json
    product.ProductName = data['ProductName']
    product.ProductCode = data['ProductCode']
    product.UnitPrice = data['UnitPrice']
    product.QuantityPerUnit = data['QuantityPerUnit']
    db.session.commit()
    return jsonify(product.to_dict())

@product_bp.route('/<int:ProductID>', methods=['DELETE'])
def delete_product(ProductID):
    try:
        # Delete related order details
        OrderDetail.query.filter_by(ProductID=ProductID).delete()
        # Delete related purchase order details
        PurchaseOrderDetail.query.filter_by(ProductID=ProductID).delete()
        # Delete related product vendors
        ProductVendor.query.filter_by(ProductID=ProductID).delete()
        product = Product.query.get_or_404(ProductID)
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully.'}), 200
    except Exception as e:
        import traceback
        db.session.rollback()
        print(traceback.format_exc())
        return jsonify({'error': 'Failed to delete product.', 'details': str(e)}), 400
