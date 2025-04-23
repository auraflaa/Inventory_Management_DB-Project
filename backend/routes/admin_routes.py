from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from models.admin_user import AdminUser
from models import db
from services.auth_service import verify_admin_login
from services.admin_service import get_all_customers, get_all_orders, get_all_products

admin_bp = Blueprint('admin_routes', __name__, url_prefix='/api/admins')
admin_blueprint = Blueprint('admin', __name__)

@admin_bp.route('/', methods=['GET'])
def get_admins():
    admins = AdminUser.query.all()
    return jsonify([{
        "AdminID": admin.AdminID,
        "Username": admin.Username,
        "EmployeeID": admin.EmployeeID
    } for admin in admins])

@admin_bp.route('/<int:AdminID>', methods=['GET'])
def get_admin(AdminID):
    admin = AdminUser.query.get_or_404(AdminID)
    return jsonify(admin.to_dict())

@admin_bp.route('/', methods=['POST'])
def create_admin():
    data = request.json
    new_admin = AdminUser(
        Username=data['Username'],
        PasswordHash=data['PasswordHash'],
        EmployeeID=data['EmployeeID']
    )
    db.session.add(new_admin)
    db.session.commit()
    return jsonify(new_admin.to_dict()), 201

@admin_bp.route('/<int:AdminID>', methods=['PUT'])
def update_admin(AdminID):
    admin = AdminUser.query.get_or_404(AdminID)
    data = request.json
    admin.Username = data['Username']
    admin.PasswordHash = data['PasswordHash']
    admin.EmployeeID = data['EmployeeID']
    db.session.commit()
    return jsonify(admin.to_dict())

@admin_bp.route('/<int:AdminID>', methods=['DELETE'])
def delete_admin(AdminID):
    admin = AdminUser.query.get_or_404(AdminID)
    db.session.delete(admin)
    db.session.commit()
    return '', 204

# Admin Login Route
@admin_blueprint.route('/login', methods=['POST'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')
    if verify_admin_login(username, password):
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('admin_login.html', error="Wrong username or password")

@admin_blueprint.route('/login', methods=['GET'])
def admin_login_get():
    # Render the admin login page for GET requests
    return render_template('admin_login.html')

# Admin Dashboard Route
@admin_blueprint.route('/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    from models.product import Product
    from models.company import Company
    from models.product_vendor import ProductVendor
    products = get_all_products()
    companies = Company.query.all()
    if request.method == 'POST' and request.form.get('form_type') == 'add_product':
        pname = request.form.get('product_name')
        pcode = request.form.get('product_code')
        uprice = request.form.get('unit_price')
        qty = request.form.get('quantity_per_unit')
        vendor_id = request.form.get('vendor_id')
        if pname and pcode and uprice and qty and vendor_id:
            new_product = Product(ProductName=pname, ProductCode=pcode, UnitPrice=uprice, QuantityPerUnit=qty)
            db.session.add(new_product)
            db.session.flush()  # Get ProductID
            # Link product to vendor (VendorID only)
            product_vendor = ProductVendor(ProductID=new_product.ProductID, VendorID=vendor_id)
            db.session.add(product_vendor)
            db.session.commit()
        products = get_all_products()
    return render_template('admin_dashboard.html', products=products, companies=companies)

@admin_blueprint.route('/dashboard/edit-product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    from models.product import Product
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.ProductName = request.form.get('product_name')
        product.ProductCode = request.form.get('product_code')
        product.UnitPrice = request.form.get('unit_price')
        product.QuantityPerUnit = request.form.get('quantity_per_unit')
        db.session.commit()
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('edit_product_form.html', product=product)

@admin_blueprint.route('/customers', methods=['GET'])
def admin_customers():
    customers = get_all_customers()
    return render_template('admin_customers.html', customers=customers)

@admin_blueprint.route('/customers/view', methods=['GET'])
def admin_view_customer():
    from models.customer import Customer
    from models.order import Order
    from models.order_status import OrderStatus
    customer_id = request.args.get('customer_id')
    customers = get_all_customers()
    selected_customer = None
    customer_orders = []
    if customer_id:
        selected_customer = Customer.query.get(customer_id)
        if selected_customer:
            order_status_map = {s.OrderStatusID: s.OrderStatusName for s in OrderStatus.query.all()}
            orders = Order.query.filter_by(CustomerID=customer_id).all()
            customer_orders = [
                {
                    'id': o.OrderID,
                    'status': order_status_map.get(o.OrderStatusID, 'Unknown'),
                    'date': o.OrderDate.strftime('%Y-%m-%d') if o.OrderDate else ''
                } for o in orders
            ]
    return render_template('admin_customers.html', customers=customers, selected_customer=selected_customer, customer_orders=customer_orders)

@admin_blueprint.route('/vendors', methods=['GET', 'POST'])
def admin_vendors():
    from models.company import Company
    message = None
    if request.method == 'POST':
        name = request.form.get('vendor_name')
        phone = request.form.get('vendor_phone')
        address = request.form.get('vendor_address')
        city = request.form.get('vendor_city')
        state = request.form.get('vendor_state')
        if name:
            new_vendor = Company(CompanyName=name, BusinessPhone=phone, Address=address, City=city, StateAbbrev=state)
            db.session.add(new_vendor)
            db.session.commit()
            message = 'Vendor added successfully.'
    vendors = Company.query.all()
    return render_template('admin_vendors.html', vendors=vendors, message=message)

@admin_blueprint.route('/companies', methods=['GET', 'POST'])
def admin_companies():
    from models.company import Company
    message = None
    if request.method == 'POST':
        name = request.form.get('company_name')
        phone = request.form.get('company_phone')
        address = request.form.get('company_address')
        city = request.form.get('company_city')
        state = request.form.get('company_state')
        if name:
            new_company = Company(CompanyName=name, BusinessPhone=phone, Address=address, City=city, StateAbbrev=state)
            db.session.add(new_company)
            db.session.commit()
            message = 'Company added successfully.'
    companies = Company.query.all()
    return render_template('admin_companies.html', companies=companies, message=message)