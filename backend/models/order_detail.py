from . import db

class OrderDetail(db.Model):
    __tablename__ = 'OrderDetails'
    OrderDetailID = db.Column(db.Integer, primary_key=True)
    OrderID = db.Column(db.Integer, db.ForeignKey('Orders.OrderID'), nullable=False)
    ProductID = db.Column(db.Integer, db.ForeignKey('Products.ProductID'), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)
    UnitPrice = db.Column(db.Numeric(10, 2))
    Discount = db.Column(db.Numeric(5, 2), default=0)

    def to_dict(self):
        return {
            "OrderDetailID": self.OrderDetailID,
            "OrderID": self.OrderID,
            "ProductID": self.ProductID,
            "Quantity": self.Quantity,
            "UnitPrice": str(self.UnitPrice),
            "Discount": str(self.Discount)
        }