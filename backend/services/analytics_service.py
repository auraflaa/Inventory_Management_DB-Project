from models import db
from models.customer import Customer
from models.order import Order
from models.product import Product
from models.order_detail import OrderDetail
from sqlalchemy import func, distinct

def get_analytics_data():
    """Get all analytics data for the admin dashboard"""
    
    # Total number of customers
    total_customers = db.session.query(func.count(Customer.CustomerID)).scalar()
    
    # Number of active customers (customers with at least one non-canceled order)
    active_customers = db.session.query(
        func.count(distinct(Order.CustomerID))
    ).filter(
        Order.OrderStatusID != 4  # Exclude canceled orders
    ).scalar()
    
    # Total number of pending orders (OrderStatusID 1 is pending)
    pending_orders = db.session.query(
        func.count(Order.OrderID)
    ).filter(
        Order.OrderStatusID == 1
    ).scalar()
    
    # Total number of products
    total_products = db.session.query(func.count(Product.ProductID)).scalar()
    
    # Get product sales data from completed orders, excluding canceled orders
    product_sales = db.session.query(
        Product.ProductID,
        Product.ProductName,
        Product.UnitPrice,
        Product.QuantityPerUnit,
        func.coalesce(func.sum(OrderDetail.Quantity), 0).label('total_sold')
    ).outerjoin(
        OrderDetail,
        Product.ProductID == OrderDetail.ProductID
    ).outerjoin(
        Order,
        OrderDetail.OrderID == Order.OrderID
    ).filter(
        # Only include orders that are not canceled (or NULL for products with no orders)
        db.or_(
            Order.OrderStatusID == None,  # For products with no orders
            Order.OrderStatusID != 4      # Exclude canceled orders
        )
    ).group_by(
        Product.ProductID,
        Product.ProductName,
        Product.UnitPrice,
        Product.QuantityPerUnit
    ).all()
    
    # Convert product stats to list of dictionaries
    stock_data = [
        {
            'name': p.ProductName,
            'unit_price': float(p.UnitPrice) if p.UnitPrice else 0,
            'units_in_stock': int(p.QuantityPerUnit) if p.QuantityPerUnit and str(p.QuantityPerUnit).isdigit() else 0,
            'total_sold': int(p.total_sold)
        }
        for p in product_sales
    ]
    
    # Sort by total sold in descending order
    stock_data.sort(key=lambda x: x['total_sold'], reverse=True)
    
    return {
        'total_customers': total_customers,
        'active_customers': active_customers,
        'pending_orders': pending_orders,
        'total_products': total_products,
        'product_stock': stock_data
    }

def test_analytics_queries():
    """Test function to verify analytics queries are working"""
    try:
        analytics = get_analytics_data()
        print("Analytics data retrieved successfully:")
        print(f"Total customers: {analytics['total_customers']}")
        print(f"Active customers: {analytics['active_customers']}")
        print(f"Pending orders: {analytics['pending_orders']}")
        print(f"Total products: {analytics['total_products']}")
        print(f"Number of products with stock data: {len(analytics['product_stock'])}")
        return True
    except Exception as e:
        print(f"Error testing analytics: {str(e)}")
        return False
