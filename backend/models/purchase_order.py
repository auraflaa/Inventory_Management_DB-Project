from . import db

class PurchaseOrder(db.Model):
    __tablename__ = 'PurchaseOrders'
    PurchaseOrderID = db.Column(db.Integer, primary_key=True)
    VendorID = db.Column(db.Integer, db.ForeignKey('Companies.CompanyID'), nullable=False)
    SubmittedBy = db.Column(db.Integer, db.ForeignKey('Employees.EmployeeID'), nullable=False)
    ApprovedBy = db.Column(db.Integer, db.ForeignKey('Employees.EmployeeID'))
    OrderDate = db.Column(db.DateTime, default=db.func.current_timestamp())
    StatusID = db.Column(db.Integer, db.ForeignKey('OrderStatus.OrderStatusID'), nullable=False)
    PaymentMethod = db.Column(db.String(50))

    def to_dict(self):
        return {
            "PurchaseOrderID": self.PurchaseOrderID,
            "VendorID": self.VendorID,
            "SubmittedBy": self.SubmittedBy,
            "ApprovedBy": self.ApprovedBy,
            "OrderDate": self.OrderDate,
            "StatusID": self.StatusID,
            "PaymentMethod": self.PaymentMethod
        }