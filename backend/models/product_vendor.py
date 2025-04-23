from . import db

class ProductVendor(db.Model):
    __tablename__ = 'ProductVendors'
    ProductVendorID = db.Column(db.Integer, primary_key=True)
    ProductID = db.Column(db.Integer, db.ForeignKey('Products.ProductID'), nullable=False)
    VendorID = db.Column(db.Integer, db.ForeignKey('Companies.CompanyID'), nullable=False)

    def to_dict(self):
        return {
            "ProductVendorID": self.ProductVendorID,
            "ProductID": self.ProductID,
            "VendorID": self.VendorID
        }