from . import db

class Employee(db.Model):
    __tablename__ = 'Employees'
    EmployeeID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(100), nullable=False)
    LastName = db.Column(db.String(100), nullable=False)
    EmailAddress = db.Column(db.String(255), unique=True)
    JobTitle = db.Column(db.String(100))
    PrimaryPhone = db.Column(db.String(20))

    def to_dict(self):
        return {
            "EmployeeID": self.EmployeeID,
            "FirstName": self.FirstName,
            "LastName": self.LastName,
            "EmailAddress": self.EmailAddress,
            "JobTitle": self.JobTitle,
            "PrimaryPhone": self.PrimaryPhone
        }