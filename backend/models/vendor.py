from . import db

class Vendor(db.Model):
    __tablename__ = 'Vendors'
    VendorID = db.Column(db.Integer, primary_key=True)
    VendorName = db.Column(db.String(255), nullable=False, unique=True)

    def to_dict(self):
        return {
            'VendorID': self.VendorID,
            'VendorName': self.VendorName
        }
