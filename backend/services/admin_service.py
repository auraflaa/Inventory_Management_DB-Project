from models.admin_user import AdminUser
from models import db
from models.customer import Customer
from models.order import Order
from models.product import Product

def get_all_admins():
    """Fetch all admin users."""
    return AdminUser.query.all()

def get_admin_by_id(admin_id):
    """Fetch an admin user by their ID."""
    return AdminUser.query.get_or_404(admin_id)

def create_admin(data):
    """Create a new admin user."""
    new_admin = AdminUser(
        Username=data['Username'],
        PasswordHash=data['PasswordHash'],
        EmployeeID=data['EmployeeID']
    )
    db.session.add(new_admin)
    db.session.commit()
    return new_admin

def update_admin(admin_id, data):
    """Update an existing admin user."""
    admin = AdminUser.query.get_or_404(admin_id)
    admin.Username = data['Username']
    admin.PasswordHash = data['PasswordHash']
    admin.EmployeeID = data['EmployeeID']
    db.session.commit()
    return admin

def delete_admin(admin_id):
    """Delete an admin user."""
    admin = AdminUser.query.get_or_404(admin_id)
    db.session.delete(admin)
    db.session.commit()

def get_all_customers():
    # Query the database to retrieve all customers
    customers = Customer.query.all()
    return [
        {
            "CustomerID": customer.CustomerID,
            "Name": f"{customer.FirstName} {customer.LastName}",
            "Email": customer.Email,
            "Phone": customer.Phone
        }
        for customer in customers
    ]

def get_all_orders():
    from models.order_status import OrderStatus
    order_status_map = {s.OrderStatusID: s.OrderStatusName for s in OrderStatus.query.all()}
    # Query the database to retrieve all orders
    orders = Order.query.all()
    return [
        {
            "OrderID": order.OrderID,
            "CustomerID": order.CustomerID,
            "Status": order_status_map.get(order.OrderStatusID, "Unknown"),
            "OrderDate": order.OrderDate.strftime('%Y-%m-%d') if order.OrderDate else ''
        }
        for order in orders
    ]

def get_all_products():
    # Query the database to retrieve all products
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