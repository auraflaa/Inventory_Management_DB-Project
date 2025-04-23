document.addEventListener('DOMContentLoaded', function () {
    const errorMessage = document.getElementById('error-message');
    if (errorMessage && errorMessage.textContent.trim() !== '') {
        alert(errorMessage.textContent);
    }
});

// Fetch and display customers for the admin dashboard
fetch('/api/customers')
    .then(response => response.json())
    .then(customers => {
        const customerTable = document.querySelector('#customer-table tbody');
        customers.forEach(customer => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${customer.name}</td>
                <td>${customer.email}</td>
                <td>${customer.phone}</td>
            `;
            customerTable.appendChild(row);
        });
    });

// Fetch and display orders for the admin dashboard
fetch('/api/orders')
    .then(response => response.json())
    .then(orders => {
        const orderTable = document.querySelector('#order-table tbody');
        orders.forEach(order => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${order.id}</td>
                <td>${order.customer}</td>
                <td>${order.status}</td>
                <td><a href="/admin/order/${order.id}">View Details</a></td>
            `;
            orderTable.appendChild(row);
        });
    });

// Fetch and display products for the admin dashboard
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
            `;
            productTable.appendChild(row);
        });
    });

function openEditModal(productId, name, code, price, quantity) {
    document.getElementById('editProductModal').style.display = 'block';
    document.getElementById('edit_product_id').value = productId;
    document.getElementById('edit_product_name').value = name;
    document.getElementById('edit_product_code').value = code;
    document.getElementById('edit_unit_price').value = price;
    document.getElementById('edit_quantity_per_unit').value = quantity;
    document.getElementById('editProductForm').action = `/admin/dashboard/edit-product/${productId}`;
}

function closeEditModal() {
    document.getElementById('editProductModal').style.display = 'none';
}

function deleteProduct(productId) {
    if (!confirm('Are you sure you want to delete this product?')) return;
    fetch(`/api/products/${productId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (response.ok) {
            location.reload();
        } else {
            response.text().then(text => alert('Failed to delete product: ' + text));
        }
    })
    .catch(error => {
        alert('Error deleting product: ' + error);
    });
}

window.onclick = function(event) {
    var modal = document.getElementById('editProductModal');
    if (event.target == modal) {
        closeEditModal();
    }
}