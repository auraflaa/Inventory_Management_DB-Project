// Fetch and display products for the customer dashboard
fetch('/api/products')
    .then(response => response.json())
    .then(products => {
        const productTable = document.querySelector('#product-table tbody');
        products.forEach(product => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${product.name}</td>
                <td>${product.vendor}</td>
                <td>${product.company}</td>
                <td>${product.details}</td>
            `;
            productTable.appendChild(row);
        });
    });

// Fetch and display orders for the customer dashboard
fetch('/api/orders')
    .then(response => response.json())
    .then(orders => {
        const orderTable = document.querySelector('#order-table tbody');
        orders.forEach(order => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${order.id}</td>
                <td>${order.date}</td>
                <td>${order.status}</td>
                <td><a href="/customer/order/${order.id}">View Details</a></td>
            `;
            orderTable.appendChild(row);
        });
    });