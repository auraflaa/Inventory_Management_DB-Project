from . import db

class Product(db.Model):
    __tablename__ = 'Products'
    ProductID = db.Column(db.Integer, primary_key=True)
    ProductName = db.Column(db.String(255), nullable=False)
    ProductCode = db.Column(db.String(50), unique=True)
    UnitPrice = db.Column(db.Numeric(10, 2))
    QuantityPerUnit = db.Column(db.String(50))
    CompanyID = db.Column(db.Integer, db.ForeignKey('Companies.CompanyID', ondelete='CASCADE'), nullable=False)    # No need to define the relationship here since it's handled by the backref in Company model

    def to_dict(self):
        return {
            "ProductID": self.ProductID,
            "ProductName": self.ProductName,
            "ProductCode": self.ProductCode,
            "UnitPrice": str(self.UnitPrice),
            "QuantityPerUnit": self.QuantityPerUnit,
            "CompanyID": self.CompanyID,
            "CompanyName": self.company.CompanyName if self.company else None
        }
