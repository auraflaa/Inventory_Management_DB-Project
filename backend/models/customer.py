from . import db

class Customer(db.Model):
    __tablename__ = 'Customers'
    CustomerID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(100))
    LastName = db.Column(db.String(100))
    Email = db.Column(db.String(255), unique=True, nullable=False)
    Phone = db.Column(db.String(20))
    PasswordHash = db.Column(db.String(255), nullable=False)
    DefaultDarkMode = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "CustomerID": self.CustomerID,
            "FirstName": self.FirstName,
            "LastName": self.LastName,
            "Email": self.Email,
            "Phone": self.Phone
        }