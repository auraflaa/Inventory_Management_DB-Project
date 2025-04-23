from flask import Blueprint, request, jsonify
from models.order_status import OrderStatus
from models.product_vendor import ProductVendor
from models.purchase_order import PurchaseOrder
from models.purchase_order_detail import PurchaseOrderDetail
from models import db

other_bp = Blueprint('other_routes', __name__, url_prefix='/api/others')

# Routes for OrderStatus
@other_bp.route('/order-status', methods=['GET'])
def get_order_statuses():
    statuses = OrderStatus.query.all()
    return jsonify([status.to_dict() for status in statuses])

@other_bp.route('/order-status/<int:status_id>', methods=['GET'])
def get_order_status(status_id):
    status = OrderStatus.query.get_or_404(status_id)
    return jsonify(status.to_dict())

@other_bp.route('/order-status', methods=['POST'])
def create_order_status():
    data = request.json
    new_status = OrderStatus(order_status_name=data['order_status_name'])
    db.session.add(new_status)
    db.session.commit()
    return jsonify(new_status.to_dict()), 201

@other_bp.route('/order-status/<int:status_id>', methods=['PUT'])
def update_order_status(status_id):
    status = OrderStatus.query.get_or_404(status_id)
    data = request.json
    status.order_status_name = data['order_status_name']
    db.session.commit()
    return jsonify(status.to_dict())

@other_bp.route('/order-status/<int:status_id>', methods=['DELETE'])
def delete_order_status(status_id):
    status = OrderStatus.query.get_or_404(status_id)
    db.session.delete(status)
    db.session.commit()
    return '', 204

# Routes for ProductVendors
@other_bp.route('/product-vendors', methods=['GET'])
def get_product_vendors():
    vendors = ProductVendor.query.all()
    return jsonify([vendor.to_dict() for vendor in vendors])

@other_bp.route('/product-vendors/<int:vendor_id>', methods=['GET'])
def get_product_vendor(vendor_id):
    vendor = ProductVendor.query.get_or_404(vendor_id)
    return jsonify(vendor.to_dict())

# Routes for PurchaseOrders
@other_bp.route('/purchase-orders', methods=['GET'])
def get_purchase_orders():
    orders = PurchaseOrder.query.all()
    return jsonify([order.to_dict() for order in orders])

@other_bp.route('/purchase-orders/<int:order_id>', methods=['GET'])
def get_purchase_order(order_id):
    order = PurchaseOrder.query.get_or_404(order_id)
    return jsonify(order.to_dict())

# Routes for PurchaseOrderDetails
@other_bp.route('/purchase-order-details', methods=['GET'])
def get_purchase_order_details():
    details = PurchaseOrderDetail.query.all()
    return jsonify([detail.to_dict() for detail in details])

@other_bp.route('/purchase-order-details/<int:detail_id>', methods=['GET'])
def get_purchase_order_detail(detail_id):
    detail = PurchaseOrderDetail.query.get_or_404(detail_id)
    return jsonify(detail.to_dict())