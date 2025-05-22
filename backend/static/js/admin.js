// Admin Dashboard JavaScript
const adminUI = {
    dropdowns: {
        init: () => {
            const dropdowns = document.querySelectorAll('.admin-dropdown');
            
            dropdowns.forEach(dropdown => {
                const trigger = dropdown.querySelector('.admin-dropdown-trigger');
                const menu = dropdown.querySelector('.admin-dropdown-menu');
                
                trigger?.addEventListener('click', (e) => {
                    e.stopPropagation();
                    menu?.classList.toggle('active');
                    
                    // Close other dropdowns
                    dropdowns.forEach(other => {
                        if (other !== dropdown) {
                            other.querySelector('.admin-dropdown-menu')?.classList.remove('active');
                        }
                    });
                });
            });

            // Close dropdowns when clicking outside
            document.addEventListener('click', () => {
                dropdowns.forEach(dropdown => {
                    dropdown.querySelector('.admin-dropdown-menu')?.classList.remove('active');
                });
            });
        }
    },

    modal: {
        open: (modalId) => {
            const modal = document.getElementById(modalId);
            modal?.classList.add('active');
            document.body.style.overflow = 'hidden';
        },
        
        close: (modalId) => {
            const modal = document.getElementById(modalId);
            modal?.classList.remove('active');
            document.body.style.overflow = '';
        },
        
        init: () => {
            // Initialize all modals
            document.querySelectorAll('.admin-modal').forEach(modal => {
                const closeBtn = modal.querySelector('.admin-modal-close');
                const modalId = modal.id;
                
                // Close button handler
                closeBtn?.addEventListener('click', () => adminUI.modal.close(modalId));
                
                // Close on background click
                modal.addEventListener('click', (e) => {
                    if (e.target === modal) {
                        adminUI.modal.close(modalId);
                    }
                });
                
                // Close on Escape key
                document.addEventListener('keydown', (e) => {
                    if (e.key === 'Escape' && modal.classList.contains('active')) {
                        adminUI.modal.close(modalId);
                    }
                });
            });
            
            // Initialize modal triggers
            document.querySelectorAll('[data-modal-target]').forEach(trigger => {
                trigger.addEventListener('click', () => {
                    const modalId = trigger.dataset.modalTarget;
                    adminUI.modal.open(modalId);
                });
            });
        }
    },

    company: {
        confirmDelete: (companyName, productCount) => {
            const message = `Are you sure you want to delete ${companyName}?\n${
                productCount > 0 ? `This will also delete ${productCount} product(s) associated with this company.` : ''
            }`;
            return confirm(message);
        }
    },

    sidebar: {
        init: () => {
            // Add toggle button for mobile
            const sidebar = document.querySelector('.admin-sidebar');
            const sidebarToggle = document.createElement('button');
            sidebarToggle.className = 'admin-sidebar-toggle';
            sidebarToggle.innerHTML = '<span class="admin-icon">☰</span>';
            document.querySelector('.admin-header')?.prepend(sidebarToggle);

            // Toggle sidebar on mobile
            sidebarToggle.addEventListener('click', () => {
                sidebar?.classList.toggle('admin-sidebar-open');
                document.body.classList.toggle('admin-sidebar-pushed');
            });

            // Close sidebar when clicking outside on mobile
            document.addEventListener('click', (e) => {
                if (window.innerWidth <= 768 && 
                    !e.target.closest('.admin-sidebar') && 
                    !e.target.closest('.admin-sidebar-toggle')) {
                    sidebar?.classList.remove('admin-sidebar-open');
                    document.body.classList.remove('admin-sidebar-pushed');
                }
            });

            // Handle window resize
            let resizeTimeout;
            window.addEventListener('resize', () => {
                clearTimeout(resizeTimeout);
                resizeTimeout = setTimeout(() => {
                    if (window.innerWidth > 768) {
                        sidebar?.classList.remove('admin-sidebar-open');
                        document.body.classList.remove('admin-sidebar-pushed');
                    }
                }, 250);
            });
        }
    },

    forms: {
        init: () => {
            document.querySelectorAll('.admin-form').forEach(form => {
                form.addEventListener('submit', (e) => {
                    if (!adminUI.forms.validateForm(form)) {
                        e.preventDefault();
                    }
                });
                
                // Real-time validation
                form.querySelectorAll('input, select, textarea').forEach(field => {
                    field.addEventListener('blur', () => {
                        adminUI.forms.validateField(field);
                    });
                });
            });
        },
        
        validateField: (field) => {
            const value = field.value.trim();
            let isValid = true;
            const errorElement = field.nextElementSibling?.classList.contains('admin-error-message') 
                ? field.nextElementSibling 
                : null;
                
            // Required field validation
            if (field.hasAttribute('required') && !value) {
                isValid = false;
                adminUI.forms.showError(field, 'This field is required', errorElement);
            }
            
            // Email validation
            if (field.type === 'email' && value && !adminUI.forms.isValidEmail(value)) {
                isValid = false;
                adminUI.forms.showError(field, 'Please enter a valid email address', errorElement);
            }
            
            if (isValid) {
                adminUI.forms.clearError(field, errorElement);
            }
            
            return isValid;
        },
        
        validateForm: (form) => {
            let isValid = true;
            form.querySelectorAll('input, select, textarea').forEach(field => {
                if (!adminUI.forms.validateField(field)) {
                    isValid = false;
                }
            });
            return isValid;
        },
        
        showError: (field, message, errorElement) => {
            field.classList.add('admin-input-error');
            if (!errorElement) {
                errorElement = document.createElement('div');
                errorElement.className = 'admin-error-message';
                field.parentNode.insertBefore(errorElement, field.nextSibling);
            }
            errorElement.textContent = message;
        },
        
        clearError: (field, errorElement) => {
            field.classList.remove('admin-input-error');
            if (errorElement) {
                errorElement.textContent = '';
            }
        },
        
        isValidEmail: (email) => {
            return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
        }
    },

    notifications: {
        show: (message, type = 'success') => {
            const notification = document.createElement('div');
            notification.className = `admin-notification admin-notification-${type}`;
            notification.innerHTML = `
                <div class="admin-notification-content">
                    ${message}
                </div>
                <button class="admin-notification-close">&times;</button>
            `;
            
            document.body.appendChild(notification);
            
            // Add active class after a brief delay for animation
            setTimeout(() => notification.classList.add('active'), 10);
            
            // Auto-hide after 5 seconds
            setTimeout(() => {
                notification.classList.remove('active');
                setTimeout(() => notification.remove(), 300);
            }, 5000);
            
            // Close button handler
            notification.querySelector('.admin-notification-close').addEventListener('click', () => {
                notification.classList.remove('active');
                setTimeout(() => notification.remove(), 300);
            });
        }
    },

    loading: {
        show: (element) => {
            const loading = document.createElement('div');
            loading.className = 'admin-loading';
            loading.innerHTML = `
                <div class="admin-loading-spinner"></div>
                <div class="admin-loading-text">Loading...</div>
            `;
            
            // If an element is provided, make it relative and append loading
            if (element) {
                const computedStyle = window.getComputedStyle(element);
                if (computedStyle.position === 'static') {
                    element.style.position = 'relative';
                }
                element.classList.add('admin-loading-relative');
                element.appendChild(loading);
            } else {
                // Otherwise show full screen loading
                loading.classList.add('admin-loading-fullscreen');
                document.body.appendChild(loading);
            }
            return loading;
        },
        
        hide: (loadingElement) => {
            if (loadingElement) {
                const parent = loadingElement.parentElement;
                loadingElement.remove();
                if (parent?.classList.contains('admin-loading-relative')) {
                    parent.classList.remove('admin-loading-relative');
                    if (parent.style.position === 'relative') {
                        parent.style.position = '';
                    }
                }
            }
        }
    }
};

// Initialize admin UI components when DOM is loaded
document.addEventListener('DOMContentLoaded', function () {
    // Initialize all admin UI components
    adminUI.dropdowns.init();
    adminUI.modal.init();
    adminUI.forms.init();
    adminUI.sidebar.init();

    // Handle error messages with notifications
    const errorMessage = document.getElementById('error-message');
    if (errorMessage && errorMessage.textContent.trim() !== '') {
        adminUI.notifications.show(errorMessage.textContent, 'error');
    }

    // Add loading indicators to forms
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            if (this.checkValidity()) {
                const submitButton = this.querySelector('[type="submit"]');
                if (submitButton) {
                    submitButton.disabled = true;
                    const originalText = submitButton.textContent;
                    submitButton.innerHTML = '<span class="admin-loading-dots"></span>';
                    
                    // Re-enable button after a timeout (in case of network error)
                    setTimeout(() => {
                        submitButton.disabled = false;
                        submitButton.textContent = originalText;
                    }, 30000);
                }
                
                // Show loading on form container
                const formContainer = this.closest('.admin-section-card') || this.closest('.admin-modal-content');
                if (formContainer) {
                    adminUI.loading.show(formContainer);
                }
            }
        });
    });

    // Handle button loading states
    document.querySelectorAll('.admin-action-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            if (this.getAttribute('onclick')?.includes('deleteProduct')) {
                return;
            }
            const originalContent = this.innerHTML;
            this.disabled = true;
            this.innerHTML = '<span class="admin-loading-dots"></span>';
            
            setTimeout(() => {
                this.disabled = false;
                this.innerHTML = originalContent;
            }, 30000);
        });
    });
});

// Enhanced fetch function with loading state
async function fetchWithLoading(url, options = {}) {
    const loadingElement = adminUI.loading.show();
    try {
        const response = await fetch(url, options);
        adminUI.loading.hide(loadingElement);
        return response;
    } catch (error) {
        adminUI.loading.hide(loadingElement);
        throw error;
    }
}

// Enhanced database action functions with loading states
function openEditModal(productId, name, code, price, quantity) {
    const modal = document.getElementById('editProductModal');
    modal.style.display = 'block';
    modal.classList.add('active');
    document.getElementById('edit_product_id').value = productId;
    document.getElementById('edit_product_name').value = name;
    document.getElementById('edit_product_code').value = code;
    document.getElementById('edit_unit_price').value = price;
    document.getElementById('edit_quantity_per_unit').value = quantity;
    document.getElementById('editProductForm').action = `/admin/dashboard/edit-product/${productId}`;
    document.body.style.overflow = 'hidden';
}

function closeEditModal() {
    const modal = document.getElementById('editProductModal');
    modal.style.display = 'none';
    modal.classList.remove('active');
    document.body.style.overflow = '';
}

function deleteProduct(productId) {
    if (!confirm('Are you sure you want to delete this product?')) return;
    
    fetchWithLoading(`/api/products/${productId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (response.ok) {
            adminUI.notifications.show('Product deleted successfully', 'success');
            location.reload();
        } else {
            response.text().then(text => {
                adminUI.notifications.show('Failed to delete product: ' + text, 'error');
            });
        }
    })
    .catch(error => {
        adminUI.notifications.show('Error deleting product: ' + error, 'error');
    });
}