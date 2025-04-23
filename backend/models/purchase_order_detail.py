from . import db

class PurchaseOrderDetail(db.Model):
    __tablename__ = 'PurchaseOrderDetails'
    PurchaseOrderDetailID = db.Column(db.Integer, primary_key=True)
    PurchaseOrderID = db.Column(db.Integer, db.ForeignKey('PurchaseOrders.PurchaseOrderID'), nullable=False)
    ProductID = db.Column(db.Integer, db.ForeignKey('Products.ProductID'), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)
    UnitCost = db.Column(db.Numeric(10, 2))
    ReceivedDate = db.Column(db.DateTime)

    def to_dict(self):
        return {
            "PurchaseOrderDetailID": self.PurchaseOrderDetailID,
            "PurchaseOrderID": self.PurchaseOrderID,
            "ProductID": self.ProductID,
            "Quantity": self.Quantity,
            "UnitCost": str(self.UnitCost),
            "ReceivedDate": self.ReceivedDate
        }