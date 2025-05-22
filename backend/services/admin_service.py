from models.admin_user import AdminUser
from models.company import Company
from models.customer import Customer
from models.order import Order
from models.product import Product
from models import db
from sqlalchemy.exc import IntegrityError

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
    """Fetch all customers with their order counts."""
    customers = Customer.query.all()
    result = []
    for customer in customers:
        # Count orders for each customer
        order_count = Order.query.filter_by(CustomerID=customer.CustomerID).count()
        result.append({
            "CustomerID": customer.CustomerID,
            "Name": f"{customer.FirstName} {customer.LastName}",
            "Email": customer.Email,
            "Phone": customer.Phone,
            "OrderCount": order_count
        })
    return result

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

def get_all_companies():
    """Fetch all companies with their product counts."""
    companies = Company.query.all()
    return [{
        "CompanyID": company.CompanyID,
        "CompanyName": company.CompanyName,
        "BusinessPhone": company.BusinessPhone,
        "Address": company.Address,
        "City": company.City,
        "StateAbbrev": company.StateAbbrev,
        "ProductCount": len(company.products)
    } for company in companies]

def delete_company_with_products(company_id):
    """Delete a company and its associated products."""
    try:
        company = Company.query.get_or_404(company_id)
        product_count = len(company.products)
        company_name = company.CompanyName

        # The products will be automatically deleted due to cascade='all, delete-orphan'
        # in the Company model's products relationship
        db.session.delete(company)
        db.session.commit()

        return {
            'success': True,
            'message': f'Company "{company_name}" and its {product_count} product(s) have been deleted successfully',
            'name': company_name,
            'product_count': product_count
        }
    except Exception as e:
        db.session.rollback()
        return {
            'success': False,
            'message': f'Error deleting company: {str(e)}'
        }

def add_company(data):
    """Add a new company."""
    try:
        if not data.get('company_name'):
            return {
                'success': False,
                'message': 'Company name is required'
            }

        new_company = Company(
            CompanyName=data['company_name'],
            BusinessPhone=data.get('company_phone'),
            Address=data.get('company_address'),
            City=data.get('company_city'),
            StateAbbrev=data.get('company_state')
        )
        db.session.add(new_company)
        db.session.commit()

        return {
            'success': True,
            'message': f'Company "{data["company_name"]}" has been added successfully',
            'company': new_company
        }
    except IntegrityError:
        db.session.rollback()
        return {
            'success': False,
            'message': 'A company with this name already exists'
        }
    except Exception as e:
        db.session.rollback()
        return {
            'success': False,
            'message': f'Error adding company: {str(e)}'
        }