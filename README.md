# Inventory Management Database Project

## Overview

This is a dual-purpose Inventory Management System project designed for both **customers** and **administrators**. Customers can use the interface to place and track orders, while administrators manage product inventories, vendors, purchase orders, and more.

Built for academic and practical learning purposes, this system offers a realistic demonstration of backend database interaction and operational inventory control in a structured, relational schema.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **Customer Interface**: Allows placing, viewing, and tracking orders.
- **Admin Dashboard**: Manages stock, orders, vendors, employees, and purchase flows.
- **Modular Design**: Clear separation of customer and admin responsibilities.
- **Database-Centric**: Structured around a normalized and relational schema.
- **Authentication**: Simple role-based access to prevent unauthorized actions.
- **Reporting**: Generate insights through transactional records and inventory logs.

## Technologies Used

- **Frontend**: [Specify if applicable, e.g., HTML/CSS, Bootstrap]
- **Backend**: Python with Flask
- **Database**: MySQL (connected via SQLAlchemy and Flask-MySQLAlchemy)
- **Development Environment**: Python virtual environments (`venv`)
- **Version Control**: Git & GitHub

## Installation

> **Important:** A Python virtual environment must be set inside the `backend/` directory before installing dependencies.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/auraflaa/Inventory_Management_DB-Project.git
   ```

2. **Navigate to the backend folder**:
   ```bash
   cd Inventory_Management_DB-Project/backend
   ```

3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

4. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

5. **Install the required Python packages**:
   ```bash
   pip install -r requirements.txt
   ```

6. **Set up the database**:
   - Create a database (e.g., `inventory_db`) in MySQL Workbench.
   - Run the provided schema scripts to initialize tables.

7. **Environment Variables**:
   - Create a `.env` file and define MySQL credentials and other config variables.

## Usage

### For Admin
1. Start the server:
   ```bash
   python app.py
   ```
2. Access the admin panel:
   ```
   http://localhost:5000/admin
   ```
3. Log in with admin credentials to manage inventory, vendors, and employees.

### For Customer
1. Navigate to:
   ```
   http://localhost:5000/
   ```
2. Create or log in with a customer account to browse and place orders.

## Database Schema

The project is designed with a fully normalized SQL schema, consisting of:

- `Products`
- `Orders`
- `OrderStatus`
- `OrderDetails`
- `ProductVendors`
- `Companies`
- `PurchaseOrders`
- `PurchaseOrderDetails`
- `Employees`

> ER diagrams and SQL schema files are provided in the `database/` folder.

## Contributing

1. Fork this repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Make your changes, add tests if relevant.
4. Commit and push:
   ```bash
   git commit -m "Add feature"
   git push origin feature/your-feature
   ```
5. Open a pull request.

## License

This project is open-source and available under the [MIT License](LICENSE).

## Contact

- **Author**: Priyangshu  
- **GitHub**: [auraflaa](https://github.com/auraflaa)  
- **Email**: priyangshumukherjee07@gmail.com 
- **LinkedIn**: [Priyangshu Mukherjee](https://www.linkedin.com/in/priyangshu-mukherjee/)
