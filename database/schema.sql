CREATE DATABASE IF NOT EXISTS inventory_management;
USE inventory_management;
ALTER TABLE Customers ADD COLUMN DefaultDarkMode BOOLEAN DEFAULT 0;

CREATE TABLE Products (
    ProductID INT PRIMARY KEY AUTO_INCREMENT,
    ProductName VARCHAR(255) NOT NULL,
    ProductCode VARCHAR(50) UNIQUE,
    UnitPrice DECIMAL(10,2),
    QuantityPerUnit VARCHAR(50)
);

-- Independent Tables
CREATE TABLE OrderStatus (
    OrderStatusID INT PRIMARY KEY AUTO_INCREMENT,
    OrderStatusName VARCHAR(50) NOT NULL
);

CREATE TABLE Companies (
    CompanyID INT PRIMARY KEY AUTO_INCREMENT,
    CompanyName VARCHAR(255) NOT NULL,
    BusinessPhone VARCHAR(20),
    Address TEXT,
    City VARCHAR(100),
    StateAbbrev VARCHAR(10)
);

CREATE TABLE Employees (
    EmployeeID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(100) NOT NULL,
    LastName VARCHAR(100) NOT NULL,
    EmailAddress VARCHAR(255) UNIQUE,
    JobTitle VARCHAR(100),
    PrimaryPhone VARCHAR(20)
);

CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(100),
    LastName VARCHAR(100),
    Email VARCHAR(255) NOT NULL UNIQUE,
    Phone VARCHAR(20),
    PasswordHash VARCHAR(255) NOT NULL
);

-- Admin Authentication
CREATE TABLE AdminUsers (
    AdminID INT PRIMARY KEY AUTO_INCREMENT,
    Username VARCHAR(255) UNIQUE NOT NULL,
    PasswordHash VARCHAR(255) NOT NULL,
    EmployeeID INT NULL,
    FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID)
);

-- Order System
CREATE TABLE Orders (
    OrderID INT PRIMARY KEY AUTO_INCREMENT,
    EmployeeID INT,
    CustomerID INT NOT NULL,
    OrderDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    ShippedDate DATETIME,
    OrderStatusID INT NOT NULL,
    PaymentMethod VARCHAR(50),
    FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (OrderStatusID) REFERENCES OrderStatus(OrderStatusID)
);

CREATE TABLE OrderDetails (
    OrderDetailID INT PRIMARY KEY AUTO_INCREMENT,
    OrderID INT NOT NULL,
    ProductID INT NOT NULL,
    Quantity INT NOT NULL,
    UnitPrice DECIMAL(10,2),
    Discount DECIMAL(5,2) DEFAULT 0,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

-- Vendor Relationships
CREATE TABLE ProductVendors (
    ProductVendorID INT PRIMARY KEY AUTO_INCREMENT,
    ProductID INT NOT NULL,
    VendorID INT NOT NULL,
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID),
    FOREIGN KEY (VendorID) REFERENCES Companies(CompanyID)
);

-- Purchase Orders
CREATE TABLE PurchaseOrders (
    PurchaseOrderID INT PRIMARY KEY AUTO_INCREMENT,
    VendorID INT NOT NULL,
    SubmittedBy INT NOT NULL,
    ApprovedBy INT,
    OrderDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    StatusID INT NOT NULL,
    PaymentMethod VARCHAR(50),
    FOREIGN KEY (VendorID) REFERENCES Companies(CompanyID),
    FOREIGN KEY (SubmittedBy) REFERENCES Employees(EmployeeID),
    FOREIGN KEY (ApprovedBy) REFERENCES Employees(EmployeeID),
    FOREIGN KEY (StatusID) REFERENCES OrderStatus(OrderStatusID)
);

CREATE TABLE PurchaseOrderDetails (
    PurchaseOrderDetailID INT PRIMARY KEY AUTO_INCREMENT,
    PurchaseOrderID INT NOT NULL,
    ProductID INT NOT NULL,
    Quantity INT NOT NULL,
    UnitCost DECIMAL(10,2),
    ReceivedDate DATETIME,
    FOREIGN KEY (PurchaseOrderID) REFERENCES PurchaseOrders(PurchaseOrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

