from . import db

class AdminUser(db.Model):
    __tablename__ = 'AdminUsers'
    AdminID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(255), unique=True, nullable=False)
    PasswordHash = db.Column(db.String(255), nullable=False)
    EmployeeID = db.Column(db.Integer, db.ForeignKey('employees.EmployeeID'))

    def to_dict(self):
        return {
            "AdminID": self.AdminID,
            "Username": self.Username,
            "EmployeeID": self.EmployeeID
        }