from . import db

class Company(db.Model):
    __tablename__ = 'Companies'
    CompanyID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CompanyName = db.Column(db.String(255), nullable=False)
    BusinessPhone = db.Column(db.String(20))
    Address = db.Column(db.Text)
    City = db.Column(db.String(100))
    StateAbbrev = db.Column(db.String(10))    # Add products relationship with cascade delete
    products = db.relationship('Product', 
                             backref=db.backref('company', lazy=True),
                             cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "CompanyID": self.CompanyID,
            "CompanyName": self.CompanyName,
            "BusinessPhone": self.BusinessPhone,
            "Address": self.Address,
            "City": self.City,
            "StateAbbrev": self.StateAbbrev,
            "ProductCount": len(self.products)
        }