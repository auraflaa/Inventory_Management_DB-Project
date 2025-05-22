from models.customer import Customer
from models import db
from app import app
import traceback

try:
    print("Initializing app context...")
    with app.app_context():
        print("Querying customers...")
        customers = Customer.query.all()
        print(f"Found {len(customers)} customers:")
        for customer in customers:
            print(f"ID: {customer.CustomerID}, Name: {customer.FirstName} {customer.LastName}, Email: {customer.Email}")
except Exception as e:
    print(f"Error: {str(e)}")
    print("Traceback:")
    print(traceback.format_exc())
