from . import db

class Order(db.Model):
    __tablename__ = 'Orders'
    OrderID = db.Column(db.Integer, primary_key=True)
    EmployeeID = db.Column(db.Integer, db.ForeignKey('Employees.EmployeeID'))
    CustomerID = db.Column(db.Integer, db.ForeignKey('Customers.CustomerID'), nullable=False)
    OrderDate = db.Column(db.DateTime, default=db.func.current_timestamp())
    ShippedDate = db.Column(db.DateTime)
    OrderStatusID = db.Column(db.Integer, db.ForeignKey('OrderStatus.OrderStatusID'), nullable=False)
    PaymentMethod = db.Column(db.String(50))

    def to_dict(self):
        return {
            "OrderID": self.OrderID,
            "EmployeeID": self.EmployeeID,
            "CustomerID": self.CustomerID,
            "OrderDate": self.OrderDate,
            "ShippedDate": self.ShippedDate,
            "OrderStatusID": self.OrderStatusID,
            "PaymentMethod": self.PaymentMethod
        }