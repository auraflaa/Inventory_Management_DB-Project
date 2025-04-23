from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from datetime import timedelta
from models.admin_user import AdminUser
from models import db
from models.customer import Customer

def hash_password(password):
    # No hashing, just return the plain password
    return password

def verify_password(password, password_hash):
    # Compare plain text passwords directly
    return password == password_hash

def create_token(identity, expires_in=24):
    """Create a JWT token."""
    return create_access_token(identity=identity, expires_delta=timedelta(hours=expires_in))

def verify_admin_login(username, password):
    # Query the database for the admin user
    admin = AdminUser.query.filter_by(Username=username).first()
    if admin and verify_password(password, admin.PasswordHash):  # Use hashed password check
        return True
    return False

def verify_customer_login(email, password):
    # Query the database for the customer
    customer = Customer.query.filter_by(Email=email).first()
    if customer and verify_password(password, customer.PasswordHash):  # Use hashed password check
        return True
    return False