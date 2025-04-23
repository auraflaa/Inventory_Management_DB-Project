from models.product import Product
from models import db

def get_all_products():
    """Fetch all products."""
    return Product.query.all()

def get_product_by_id(product_id):
    """Fetch a product by its ID."""
    return Product.query.get_or_404(product_id)

def create_product(data):
    """Create a new product."""
    new_product = Product(
        ProductName=data['ProductName'],
        ProductCode=data['ProductCode'],
        UnitPrice=data['UnitPrice'],
        QuantityPerUnit=data['QuantityPerUnit']
    )
    db.session.add(new_product)
    db.session.commit()
    return new_product

def update_product(product_id, data):
    """Update an existing product."""
    product = Product.query.get_or_404(product_id)
    product.ProductName = data['ProductName']
    product.ProductCode = data['ProductCode']
    product.UnitPrice = data['UnitPrice']
    product.QuantityPerUnit = data['QuantityPerUnit']
    db.session.commit()
    return product

def delete_product(product_id):
    """Delete a product."""
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()