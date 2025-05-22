from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from models.admin_user import AdminUser
from models.company import Company
from models.product import Product
from models.customer import Customer
from models.product_vendor import ProductVendor
from models import db
from services.auth_service import verify_admin_login
from services.admin_service import (
    get_all_customers, 
    get_all_orders, 
    get_all_products,
    get_all_companies,
    add_company,
    delete_company_with_products
)
from sqlalchemy.exc import IntegrityError

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
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            flash('Username and password are required', 'error')
            return render_template('admin_login.html', error="All fields are required")

        if verify_admin_login(username, password):
            return redirect(url_for('admin.admin_dashboard'))
            
        flash('Invalid username or password', 'error')
        return render_template('admin_login.html', error="Wrong username or password")
    except Exception as e:
        flash(str(e), 'error')
        return render_template('admin_login.html', error=str(e))

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
        company_id = request.form.get('company_id')
        error_message = None
        if pname and pcode and uprice and qty and company_id:
            from sqlalchemy.exc import IntegrityError
            try:
                new_product = Product(ProductName=pname, ProductCode=pcode, UnitPrice=uprice, QuantityPerUnit=qty)
                db.session.add(new_product)
                db.session.flush()  # Get ProductID
                # Link product to company (as VendorID)
                product_vendor = ProductVendor(ProductID=new_product.ProductID, VendorID=company_id)
                db.session.add(product_vendor)
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()
                if 'Duplicate entry' in str(e.orig):
                    error_message = 'Product code already exists. Please use a unique product code.'
                else:
                    error_message = 'Failed to add product. Please check your input.'
        products = get_all_products()
        return render_template('admin_dashboard.html', products=products, companies=companies, error_message=error_message)
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
    try:
        customers = get_all_customers()
        print(f"[DEBUG] Found {len(customers)} customers") # Debug print
        for customer in customers:
            print(f"[DEBUG] Customer data: {customer}")  # Debug customer data
        
        # Add flash message if we found customers
        if customers:
            flash('Successfully loaded customer data', 'success')
        else:
            flash('No customers found in the database', 'info')
            
        return render_template('admin_customers.html', customers=customers)
    except Exception as e:
        import traceback
        print(f"[ERROR] Error in admin_customers: {str(e)}")
        print(traceback.format_exc())
        flash('Failed to load customer data', 'error')
        return render_template('admin_customers.html', customers=[])

@admin_blueprint.route('/customers/<int:customer_id>', methods=['GET'])
def customer_details(customer_id):
    try:
        # Get customer details
        customer = Customer.query.get_or_404(customer_id)
        
        # Get customer orders with status
        from models.order import Order
        from models.order_status import OrderStatus
        
        # Get status mapping
        order_statuses = OrderStatus.query.all()
        status_map = {status.OrderStatusID: status.OrderStatusName for status in order_statuses}
        
        # Get orders for this customer
        orders = Order.query.filter_by(CustomerID=customer_id).all()
        order_list = []
        for order in orders:
            order_list.append({
                'id': order.OrderID,
                'status': status_map.get(order.OrderStatusID, 'Unknown'),
                'date': order.OrderDate.strftime('%Y-%m-%d %H:%M') if order.OrderDate else 'N/A'
            })
        
        # Get all customers for the table
        all_customers = get_all_customers()
        
        return render_template('admin_customers.html',
                             customers=all_customers,
                             selected_customer=customer,
                             customer_orders=order_list)
                             
    except Exception as e:
        print(f"[ERROR] Error in customer_details: {str(e)}")
        import traceback
        print(traceback.format_exc())
        flash('Error loading customer details', 'error')
        return redirect(url_for('admin.admin_customers'))

@admin_blueprint.route('/customers/order-details/<int:order_id>', methods=['GET'])
def admin_order_details(order_id):
    from models.order import Order
    from models.order_detail import OrderDetail
    from models.product import Product
    from models.company import Company
    from models.product_vendor import ProductVendor
    order = Order.query.get_or_404(order_id)
    order_details = OrderDetail.query.filter_by(OrderID=order_id).all()
    detailed_products = []
    for detail in order_details:
        product = Product.query.get(detail.ProductID)
        vendor_name = 'N/A'
        company_name = 'N/A'
        product_vendor = ProductVendor.query.filter_by(ProductID=product.ProductID).first() if product else None
        if product_vendor:
            company = Company.query.get(product_vendor.VendorID)
            if company:
                vendor_name = company.CompanyName
                company_name = company.CompanyName
        detailed_products.append({
            'ProductName': product.ProductName if product else 'N/A',
            'CompanyName': company_name,
            'VendorName': vendor_name,
            'Quantity': detail.Quantity,
            'UnitPrice': detail.UnitPrice
        })
    return render_template('admin_order_details.html', order=order, products=detailed_products)

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
    try:
        if request.method == 'POST':
            result = add_company(request.form)
            if result['success']:
                flash(result['message'], 'success')
            else:
                flash(result['message'], 'error')

        companies = get_all_companies()
        return render_template('admin_companies.html', companies=companies)
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return render_template('admin_companies.html', companies=[])

@admin_blueprint.route('/companies/delete/<int:company_id>', methods=['POST'])
def delete_company(company_id):
    result = delete_company_with_products(company_id)
    if result['success']:
        flash(result['message'], 'success')
    else:
        flash(result['message'], 'error')
    return redirect(url_for('admin.admin_companies'))