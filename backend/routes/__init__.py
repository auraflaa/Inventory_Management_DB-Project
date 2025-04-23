from flask import Blueprint

# Import route blueprints
from .product_routes import product_bp
# Add other route imports here as needed

def register_routes(app):
    # Register blueprints
    app.register_blueprint(product_bp)
    # Add other blueprints here