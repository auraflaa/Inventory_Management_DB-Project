from flask import Blueprint, request, jsonify
from models.order import Order
from models import db

order_bp = Blueprint('order_routes', __name__, url_prefix='/api/orders')

@order_bp.route('/', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([{
        "OrderID": order.OrderID,
        "EmployeeID": order.EmployeeID,
        "CustomerID": order.CustomerID,
        "OrderDate": order.OrderDate,
        "ShippedDate": order.ShippedDate,
        "OrderStatusID": order.OrderStatusID,
        "PaymentMethod": order.PaymentMethod
    } for order in orders])

@order_bp.route('/<int:OrderID>', methods=['GET'])
def get_order(OrderID):
    order = Order.query.get_or_404(OrderID)
    return jsonify(order.to_dict())

@order_bp.route('/', methods=['POST'])
def create_order():
    data = request.json
    new_order = Order(
        EmployeeID=data['EmployeeID'],
        CustomerID=data['CustomerID'],
        OrderDate=data['OrderDate'],
        ShippedDate=data['ShippedDate'],
        OrderStatusID=data['OrderStatusID'],
        PaymentMethod=data['PaymentMethod']
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify(new_order.to_dict()), 201

@order_bp.route('/<int:OrderID>', methods=['PUT'])
def update_order(OrderID):
    order = Order.query.get_or_404(OrderID)
    data = request.json
    order.EmployeeID = data['EmployeeID']
    order.CustomerID = data['CustomerID']
    order.OrderDate = data['OrderDate']
    order.ShippedDate = data['ShippedDate']
    order.OrderStatusID = data['OrderStatusID']
    order.PaymentMethod = data['PaymentMethod']
    db.session.commit()
    return jsonify(order.to_dict())

@order_bp.route('/<int:OrderID>', methods=['DELETE'])
def delete_order(OrderID):
    order = Order.query.get_or_404(OrderID)
    db.session.delete(order)
    db.session.commit()
    return '', 204