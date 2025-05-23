from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from models.admin_user import AdminUser
from models.company import Company
from models.product import Product
from models.customer import Customer
from models.product_vendor import ProductVendor
from models.order_detail import OrderDetail
from models.purchase_order_detail import PurchaseOrderDetail
from models.purchase_order import PurchaseOrder
from models import db
from services.auth_service import verify_admin_login, check_admin_login, set_admin_login
from services.admin_service import (
    get_all_customers, 
    get_all_orders, 
    get_all_products,
    get_all_companies,
    add_company,
    delete_company_with_products
)
from services.analytics_service import get_analytics_data
from sqlalchemy.exc import IntegrityError

admin_bp = Blueprint('admin_routes', __name__, url_prefix='/api/admins')
admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')

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
            set_admin_login(True)  # Set admin as logged in
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

# Admin Logout Route
@admin_blueprint.route('/logout')
def admin_logout():
    set_admin_login(False)  # Clear admin login status
    session.clear()  # Clear all session data
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('admin.admin_login'))

# Admin Dashboard Route
@admin_blueprint.route('/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    try:
        from models.product import Product
        from models.company import Company
        from models.product_vendor import ProductVendor
        
        products = get_all_products()
        companies = Company.query.all()
        
        if request.method == 'POST' and request.form.get('form_type') == 'add_product':
            # Extract form data
            pname = request.form.get('product_name')
            pcode = request.form.get('product_code')
            uprice = request.form.get('unit_price')
            qty = request.form.get('quantity_per_unit')
            company_id = request.form.get('company_id')
            
            # Validate all fields are present
            if not all([pname, pcode, uprice, qty, company_id]):
                flash('All fields are required', 'error')
                return render_template('admin_dashboard.html', products=products, companies=companies)
            
            try:
                # Create new product
                new_product = Product(
                    ProductName=pname,
                    ProductCode=pcode,
                    UnitPrice=float(uprice),
                    QuantityPerUnit=qty,
                    CompanyID=company_id  # Add CompanyID directly to product
                )
                db.session.add(new_product)
                db.session.flush()  # Get ProductID
                
                # Create product vendor relationship
                product_vendor = ProductVendor(
                    ProductID=new_product.ProductID,
                    VendorID=company_id
                )
                db.session.add(product_vendor)
                db.session.commit()
                
                flash('Product added successfully', 'success')
                products = get_all_products()  # Refresh products list
                
            except IntegrityError as e:
                db.session.rollback()
                if 'Duplicate entry' in str(e.orig):
                    flash('Product code already exists. Please use a unique product code.', 'error')
                else:
                    flash('Failed to add product. Please check your input.', 'error')
            except ValueError:
                db.session.rollback()
                flash('Invalid price value', 'error')
            except Exception as e:
                db.session.rollback()
                flash(f'An error occurred: {str(e)}', 'error')
        
        return render_template('admin_dashboard.html', products=products, companies=companies)
        
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return render_template('admin_dashboard.html', products=[], companies=[])

@admin_blueprint.route('/dashboard/edit-product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    try:
        from models.product import Product
        product = Product.query.get_or_404(product_id)
        
        if request.method == 'POST':
            # Validate inputs
            product_name = request.form.get('product_name')
            product_code = request.form.get('product_code')
            unit_price = request.form.get('unit_price')
            quantity_per_unit = request.form.get('quantity_per_unit')
            
            if not all([product_name, product_code, unit_price, quantity_per_unit]):
                flash('All fields are required', 'error')
                return render_template('edit_product_form.html', product=product)
            
            try:
                # Update product
                product.ProductName = product_name
                product.ProductCode = product_code
                product.UnitPrice = float(unit_price)
                product.QuantityPerUnit = quantity_per_unit
                
                db.session.commit()
                flash('Product updated successfully', 'dashboard-success')  # Use a different flash category
                return redirect(url_for('admin.admin_dashboard'))
                
            except ValueError:
                flash('Invalid price value', 'error')
                return render_template('edit_product_form.html', product=product)
                
        return render_template('edit_product_form.html', product=product)
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating product: {str(e)}', 'error')
        return redirect(url_for('admin.admin_dashboard'))

@admin_blueprint.route('/dashboard/delete-product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    try:
        # First delete any related records
        OrderDetail.query.filter_by(ProductID=product_id).delete()
        PurchaseOrderDetail.query.filter_by(ProductID=product_id).delete()
        ProductVendor.query.filter_by(ProductID=product_id).delete()
        
        # Then delete the product
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting product: {str(e)}', 'error')
    return redirect(url_for('admin.admin_dashboard'))

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
def customer_order_details(order_id):
    return redirect(url_for('admin.admin_order_details', order_id=order_id))
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
    if not result['success']:
        flash(result['message'], 'error')
    return redirect(url_for('admin.admin_companies'))

@admin_blueprint.route('/orders')
def admin_orders():
    # Import the required models
    from models.order import Order
    from models.customer import Customer
    from models.order_status import OrderStatus
    from datetime import datetime
    
    delivered_status_id = 3  # Status ID 3 is 'Delivered'
    
    # Base query with joins
    query = db.session.query(
        Order, 
        Customer,
        OrderStatus
    ).join(
        Customer, 
        Order.CustomerID == Customer.CustomerID
    ).join(
        OrderStatus,
        Order.OrderStatusID == OrderStatus.OrderStatusID
    )

    # Get all orders and split them based on status
    orders = query.all()
    
    # Process orders into delivered and pending lists
    delivered_orders = []
    pending_orders = []
    
    for order, customer, status in orders:
        order_info = {
            'OrderID': order.OrderID,
            'CustomerID': customer.CustomerID,
            'CustomerName': f"{customer.FirstName} {customer.LastName}",
            'OrderDate': order.OrderDate,
            'ShippedDate': order.ShippedDate,
            'OrderStatusID': order.OrderStatusID,
            'StatusName': status.OrderStatusName
        }
        
        # Orders with status 3 (Delivered) go to delivered_orders, others to pending_orders
        if order.OrderStatusID == delivered_status_id:
            delivered_orders.append(order_info)
        else:
            pending_orders.append(order_info)

    # Get all order statuses for the dropdown (Status 1-Pending, 2-Shipped, 3-Delivered)
    order_statuses = OrderStatus.query.all()

    return render_template(
        'admin_orders.html',
        pending_orders=pending_orders,
        delivered_orders=delivered_orders,
        order_statuses=order_statuses
    )

@admin_blueprint.route('/orders/<int:order_id>/status', methods=['POST'])
def update_order_status(order_id):
    try:
        from models.order import Order
        from models.order_status import OrderStatus
        from datetime import datetime

        order = Order.query.get_or_404(order_id)
        new_status = int(request.form.get('status'))
        
        # Check if current status is "Delivered" (status ID 3)
        if order.OrderStatusID == 3:
            flash("Cannot modify status of delivered orders", "error")
            return redirect(url_for('admin.admin_orders'))

        status = OrderStatus.query.get(new_status)
        if not status:
            flash("Invalid status selected", "error")
            return redirect(url_for('admin.admin_orders'))

        # Update the order status
        previous_status = order.OrderStatusID
        order.OrderStatusID = new_status
        
        # If new status is "Delivered" (status ID 3), set the shipped date
        if new_status == 3:
            if request.form.get('confirmed') != 'true':
                # Return to the orders page if not confirmed
                flash("Please confirm before marking the order as delivered", "warning")
                return redirect(url_for('admin.admin_orders'))
            order.ShippedDate = datetime.now()
            flash(f"Order #{order_id} has been marked as delivered. This action cannot be undone.", "info")
        else:
            flash(f"Order #{order_id} status updated to {status.OrderStatusName}", "success")
        
        db.session.commit()
        
    except ValueError:
        db.session.rollback()
        flash("Invalid status value provided", "error")
    except Exception as e:
        db.session.rollback()
        flash(f"Error updating order status: {str(e)}", "error")
        
    return redirect(url_for('admin.admin_orders'))

@admin_blueprint.route('/orders/<int:order_id>')
def admin_order_details(order_id):
    try:
        # Import required models
        from models.order import Order
        from models.order_detail import OrderDetail
        from models.customer import Customer
        from models.product import Product
        from models.order_status import OrderStatus
        from models.company import Company
        from models.product_vendor import ProductVendor

        # Get order and related customer information
        order = Order.query.get_or_404(order_id)
        customer = Customer.query.get_or_404(order.CustomerID)
        order_status = OrderStatus.query.get_or_404(order.OrderStatusID)
        
        # Get order details with product information
        order_details = OrderDetail.query.filter_by(OrderID=order_id).all()
        order_items = []
        total_amount = 0
        
        for detail in order_details:
            product = Product.query.get(detail.ProductID)
            company_name = 'N/A'
            
            # Get company name through product vendor relationship
            product_vendor = ProductVendor.query.filter_by(ProductID=product.ProductID).first()
            if product_vendor:
                company = Company.query.get(product_vendor.VendorID)
                if company:
                    company_name = company.CompanyName

            item = {
                'ProductName': product.ProductName,
                'CompanyName': company_name,
                'Quantity': detail.Quantity,
                'UnitPrice': detail.UnitPrice,
                'Discount': detail.Discount
            }
            order_items.append(item)
            total_amount += detail.Quantity * detail.UnitPrice * (1 - detail.Discount)

        # Get all order statuses for the dropdown
        order_statuses = OrderStatus.query.all()
        
        return render_template(
            'admin_order_details.html',
            order=order,
            customer=customer,
            order_status=order_status,
            order_items=order_items,
            order_statuses=order_statuses,
            total_amount=total_amount
        )
        
    except Exception as e:
        flash("Error loading order details", "error")
        return redirect(url_for('admin.admin_orders'))

@admin_blueprint.route('/analysis')
def admin_analysis():
    """Render the admin analysis dashboard"""
    # Verify admin is logged in using session check
    if not check_admin_login():
        flash('Please log in to access the analytics dashboard', 'error')
        return redirect(url_for('admin.admin_login'))
    
    try:
        # Test analytics queries first
        from services.analytics_service import test_analytics_queries
        if not test_analytics_queries():
            flash('Error retrieving analytics data. Please try again later.', 'error')
            return redirect(url_for('admin.admin_dashboard'))
        
        # Get analytics data
        analytics_data = get_analytics_data()
        
        return render_template(
            'admin_analysis.html',
            analytics=analytics_data
        )
    except Exception as e:
        flash(f'Error loading analytics dashboard: {str(e)}', 'error')
        return redirect(url_for('admin.admin_dashboard'))