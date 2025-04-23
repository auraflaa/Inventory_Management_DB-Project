from . import db

class OrderStatus(db.Model):
    __tablename__ = 'OrderStatus'
    OrderStatusID = db.Column(db.Integer, primary_key=True)
    OrderStatusName = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            "OrderStatusID": self.OrderStatusID,
            "OrderStatusName": self.OrderStatusName
        }