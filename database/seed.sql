USE inventory_management;

INSERT INTO Products (ProductName, ProductCode, UnitPrice, QuantityPerUnit)
VALUES ('Sample Product', 'SP001', 10.99, '10 units');

-- Insert sample data for OrderStatus
INSERT INTO OrderStatus (OrderStatusName)
VALUES ('Pending'), ('Shipped'), ('Delivered');

INSERT INTO OrderStatus (OrderStatusID, OrderStatusName)
VALUES (4, 'Cancelled');

-- Insert sample data for Companies
INSERT INTO Companies (CompanyName, BusinessPhone, Address, City, StateAbbrev)
VALUES ('Tech Supplies Inc.', '123-456-7890', '123 Tech Street', 'Tech City', 'TS');

-- Insert sample data for Employees
INSERT INTO Employees (FirstName, LastName, EmailAddress, JobTitle, PrimaryPhone)
VALUES ('John', 'Doe', 'john.doe@example.com', 'Manager', '987-654-3210');

-- Insert sample data for Customers
INSERT INTO Customers (FirstName, LastName, Email, Phone, PasswordHash)
VALUES ('Jane', 'Smith', 'jane.smith@example.com', '555-123-4567', 'hashedpassword123'),
('Alice', 'Johnson', 'alice.johnson@example.com', '555-234-5678', 'hashedpassword456'),
('Bob', 'Williams', 'bob.williams@example.com', '555-345-6789', 'hashedpassword789'),
('Charlie', 'Brown', 'charlie.brown@example.com', '555-456-7890', 'hashedpassword012');

-- Insert sample data for AdminUsers
INSERT INTO AdminUsers (Username, PasswordHash, EmployeeID)
VALUES ('admin', 'hashedadminpassword', 1),
('admin1', 'hashedadminpassword1', 1),
('admin2', 'hashedadminpassword2', 1),
('admin3', 'hashedadminpassword3', 1);

-- Insert sample data for Orders
INSERT INTO Orders (EmployeeID, CustomerID, OrderDate, ShippedDate, OrderStatusID, PaymentMethod)
VALUES (1, 1, '2025-04-01 10:00:00', '2025-04-05 15:00:00', 2, 'Credit Card'),
(1, 2, '2025-04-10 10:00:00', '2025-04-12 15:00:00', 1, 'PayPal'),
(1, 3, '2025-04-11 11:00:00', '2025-04-13 16:00:00', 2, 'Credit Card'),
(1, 4, '2025-04-12 12:00:00', '2025-04-14 17:00:00', 3, 'Bank Transfer'),
(1, 1, '2025-04-02 10:00:00', '2025-04-06 15:00:00', 1, 'Credit Card'),
(1, 1, '2025-04-03 11:00:00', '2025-04-07 16:00:00', 2, 'PayPal'),
(1, 1, '2025-04-04 12:00:00', '2025-04-08 17:00:00', 3, 'Bank Transfer'),
(1, 2, '2025-04-11 10:00:00', '2025-04-13 15:00:00', 1, 'Credit Card'),
(1, 2, '2025-04-12 11:00:00', '2025-04-14 16:00:00', 2, 'PayPal'),
(1, 2, '2025-04-13 12:00:00', '2025-04-15 17:00:00', 3, 'Bank Transfer'),
(1, 3, '2025-04-14 10:00:00', '2025-04-16 15:00:00', 1, 'Credit Card'),
(1, 3, '2025-04-15 11:00:00', '2025-04-17 16:00:00', 2, 'PayPal'),
(1, 3, '2025-04-16 12:00:00', '2025-04-18 17:00:00', 3, 'Bank Transfer'),
(1, 4, '2025-04-17 10:00:00', '2025-04-19 15:00:00', 1, 'Credit Card'),
(1, 4, '2025-04-18 11:00:00', '2025-04-20 16:00:00', 2, 'PayPal'),
(1, 4, '2025-04-19 12:00:00', '2025-04-21 17:00:00', 3, 'Bank Transfer');

-- Insert sample data for OrderDetails
INSERT INTO OrderDetails (OrderID, ProductID, Quantity, UnitPrice, Discount)
VALUES (1, 1, 2, 10.99, 0);

-- Insert sample data for ProductVendors
INSERT INTO ProductVendors (ProductID, VendorID)
VALUES (1, 1);

-- Insert sample data for PurchaseOrders
INSERT INTO PurchaseOrders (VendorID, SubmittedBy, ApprovedBy, OrderDate, StatusID, PaymentMethod)
VALUES (1, 1, 1, '2025-04-10 12:00:00', 1, 'Bank Transfer');

-- Insert sample data for PurchaseOrderDetails
INSERT INTO PurchaseOrderDetails (PurchaseOrderID, ProductID, Quantity, UnitCost, ReceivedDate)
VALUES (1, 1, 50, 8.99, '2025-04-15 14:00:00');
SELECT * FROM products;