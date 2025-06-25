# Inventory Management Database System

An end-to-end web application for managing inventory, orders, and analytics. This dual-interface system offers both customer-facing shopping features and a comprehensive administrative dashboard for back-office operations.

---

## 🔗 Live Demo & Repository

* **GitHub:** [auraflaa/Inventory\_Management\_DB-Project](https://github.com/auraflaa/Inventory_Management_DB-Project)

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Database Schema](#database-schema)
7. [Security](#security)

   * [CSRF Protection](#csrf-protection)
8. [Contributing](#contributing)
9. [License](#license)
10. [Contact](#contact)

---

## Overview

This Inventory Management Database System provides two distinct interfaces:

* **Customer Panel:**

  * Browse and search products
  * Place new orders
  * Track shipment status (Delivered / Pending / Cancelled)
  * View order history and details

* **Admin Dashboard:**

  * Manage products, vendors, employees (CRUD operations)
  * Process and update order statuses
  * Create purchase orders and manage stock inflows
  * Interactive analytics for sales trends & current inventory
  * Role-based access control for security

Built with academic rigor and practical use in mind, this project demonstrates robust database design, RESTful API development, and a full-stack Flask application.

---

## Features

* **Customer Interface**: Place, view, and track orders through a user-friendly panel.
* **Admin Dashboard**: Full control over inventory, vendors, purchase orders, and employees.
* **Modular Separation**: Clear differentiation between customer and admin routes and templates.
* **Normalized Relational Schema**: Entities include Products, Orders, OrderDetails, Vendors, PurchaseOrders, Companies, Employees.
* **RESTful Flask APIs**: Clean service layers with Flask-MySQLAlchemy ORM.
* **Interactive Reporting**: Dynamic bar charts for units sold and available stock.
* **Authentication & Authorization**: Secure, role-based login flows.

### Additional Highlights

* **Form Validation & Flash Messages**: Both server-side and client-side validation with user feedback via Flask’s `flash`.
* **Blueprint Architecture**: Organized codebase into Flask blueprints (`customer`, `admin`, `auth`) for maintainability.
* **Error Handling**: Custom 404 and 500 error pages with informative messages.
* **Search & Pagination**: Product search functionality and paginated listings for improved UX on large datasets.
* **Configuration Management**: Environment-specific settings via `.env`, with development and production modes.
* **Logging**: Structured logging setup capturing key events, errors, and user actions.
* **Extensible Design**: Easily add new modules (e.g., reporting, notifications) by following existing patterns.

---

## Technologies Used

| Component | Technology                          |
| --------- | ----------------------------------- |
| Frontend  | HTML5, CSS3, JavaScript (Jinja2)    |
| Backend   | Python 3, Flask, Flask-MySQLAlchemy |
| Database  | MySQL (InnoDB, normalized schema)   |
| Dev Tools | Git, GitHub, Python `venv`          |

---

## Installation

> Ensure you work within a Python virtual environment inside the `backend/` directory.

1. **Clone the repository**

   ```bash
   git clone https://github.com/auraflaa/Inventory_Management_DB-Project.git
   cd Inventory_Management_DB-Project/backend
   ```

2. **Create and activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   ```bash
   cp .env.example .env
   # Populate .env with your MySQL credentials and SECRET_KEY
   ```

5. **Initialize the database**

   ```bash
   python db/init_db.py  # creates tables and seed data
   ```

6. **Launch the server**

   ```bash
   flask run
   ```

---

## Usage

* **Customer Panel**: Visit `http://localhost:5000/`, sign up or log in, and browse products.
* **Admin Dashboard**: Go to `http://localhost:5000/admin`, log in with admin credentials to manage the system.

---

## Database Schema

The system is backed by a fully normalized relational MySQL database. Key tables include:

* `Products`
* `Orders`
* `OrderDetails`
* `OrderStatus`
* `ProductVendors`
* `PurchaseOrders`
* `PurchaseOrderDetails`
* `Companies`
* `Employees`

ER diagrams and initial SQL schema scripts are available under the `database/` folder.

---

## Security

We employ modern web security best practices to safeguard data and operations.

### CSRF Protection

1. **Flask-WTF Integration**

   * Form classes inherit from `FlaskForm`, automatically embedding a signed hidden `csrf_token` field.

2. **Template Inclusion**

   * Include `{{ form.csrf_token }}` in every POST form. Example:

   ```html
   <form method="POST" action="{{ url_for('admin.add_product') }}">
     {{ form.csrf_token }}
     {{ form.name.label }} {{ form.name }}
     <!-- more fields -->
     <button type="submit">Add Product</button>
   </form>
   ```

3. **Route Validation**

   * `form.validate_on_submit()` checks CSRF token and input data. Invalid tokens cause a 400 error.

4. **Secret Key Configuration**

   * A robust `SECRET_KEY` in `.env` signs CSRF tokens and session cookies:

     ```text
     SECRET_KEY=your-very-secret-key
     ```

---

## Contributing

Contributions welcome:

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m "Add your feature"`
4. Push: `git push origin feature/your-feature`
5. Open a pull request

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for full terms.

---

## Contact

* **Author**: Priyangshu Mukherjee
* **Email**: [priyangshumukherjee07@gmail.com](mailto:priyangshumukherjee07@gmail.com)
* **GitHub**: [auraflaa](https://github.com/auraflaa)
* **LinkedIn**: [Priyangshu Mukherjee](https://www.linkedin.com/in/priyangshu-mukherjee/)
