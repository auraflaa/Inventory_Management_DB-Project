from models.order import Order
from models import db

def get_all_orders():
    """Fetch all orders."""
    return Order.query.all()

def get_order_by_id(order_id):
    """Fetch an order by its ID."""
    return Order.query.get_or_404(order_id)

def create_order(data):
    """Create a new order."""
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
    return new_order

def update_order(order_id, data):
    """Update an existing order."""
    order = Order.query.get_or_404(order_id)
    order.EmployeeID = data['EmployeeID']
    order.CustomerID = data['CustomerID']
    order.OrderDate = data['OrderDate']
    order.ShippedDate = data['ShippedDate']
    order.OrderStatusID = data['OrderStatusID']
    order.PaymentMethod = data['PaymentMethod']
    db.session.commit()
    return order

def delete_order(order_id):
    """Delete an order."""
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()