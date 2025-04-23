from . import db

class Product(db.Model):
    __tablename__ = 'Products'
    ProductID = db.Column(db.Integer, primary_key=True)
    ProductName = db.Column(db.String(255), nullable=False)
    ProductCode = db.Column(db.String(50), unique=True)
    UnitPrice = db.Column(db.Numeric(10, 2))
    QuantityPerUnit = db.Column(db.String(50))

    def to_dict(self):
        return {
            "ProductID": self.ProductID,
            "ProductName": self.ProductName,
            "ProductCode": self.ProductCode,
            "UnitPrice": str(self.UnitPrice),
            "QuantityPerUnit": self.QuantityPerUnit
        }
