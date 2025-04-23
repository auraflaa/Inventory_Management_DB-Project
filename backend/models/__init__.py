from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models
from .product import Product
from .order import Order
from .customer import Customer
from .admin_user import AdminUser
from .order_status import OrderStatus
from .order_detail import OrderDetail
from .product_vendor import ProductVendor
from .purchase_order import PurchaseOrder
from .purchase_order_detail import PurchaseOrderDetail
from .company import Company
from .employee import Employee
from .vendor import Vendor