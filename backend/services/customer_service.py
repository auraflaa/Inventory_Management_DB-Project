from models.customer import Customer
from models import db
from models.order import Order
from models.product import Product

def get_all_customers():
    """Fetch all customers."""
    return Customer.query.all()

def get_customer_by_id(customer_id):
    """Fetch a customer by their ID."""
    return Customer.query.get_or_404(customer_id)

def create_customer(data):
    """Create a new customer."""
    new_customer = Customer(
        FirstName=data['FirstName'],
        LastName=data['LastName'],
        Email=data['Email'],
        Phone=data['Phone'],
        PasswordHash=data['PasswordHash']  # Should be plain text
    )
    db.session.add(new_customer)
    db.session.commit()
    return new_customer

def update_customer(customer_id, data):
    """Update an existing customer."""
    customer = Customer.query.get_or_404(customer_id)
    customer.FirstName = data['FirstName']
    customer.LastName = data['LastName']
    customer.Email = data['Email']
    customer.Phone = data['Phone']
    customer.PasswordHash = data['PasswordHash']
    db.session.commit()
    return customer

def delete_customer(customer_id):
    """Delete a customer."""
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()

def get_customer_orders(customer_id):
    orders = Order.query.filter_by(CustomerID=customer_id).all()
    from models.order_status import OrderStatus
    order_status_map = {s.OrderStatusID: s.OrderStatusName for s in OrderStatus.query.all()}
    return [
        {
            "OrderID": order.OrderID,
            "Status": order_status_map.get(order.OrderStatusID, "Unknown"),
            "OrderDate": order.OrderDate.strftime('%Y-%m-%d') if order.OrderDate else ''
        }
        for order in orders
    ]

def get_customer_products(customer_id):
    products = Product.query.all()
    return [
        {
            "ProductID": product.ProductID,
            "ProductName": product.ProductName,
            "ProductCode": product.ProductCode,
            "UnitPrice": str(product.UnitPrice),
            "QuantityPerUnit": product.QuantityPerUnit
        }
        for product in products
    ]