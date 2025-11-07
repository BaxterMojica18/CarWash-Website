let allProducts = [];

async function loadProducts() {
    try {
        const products = await API.products.getAll();
        allProducts = products;
        
        const productsList = products.filter(p => p.type === 'product');
        const grid = document.getElementById('productsGrid');
        grid.innerHTML = productsList.map(prod => `
            <div class="product-card">
                <h3>${prod.name}</h3>
                <p class="price">$${prod.price.toFixed(2)}</p>
                <p>${prod.description || ''}</p>
                <p style="color: #666; font-size: 14px; margin-top: 10px;">Stock: ${prod.quantity || 0} ${prod.quantity_unit || 'units'}</p>
                <div class="product-actions">
                    <button class="btn-edit" onclick='editProduct(${prod.id})' data-permission="manage_products">Edit</button>
                    <button class="btn-delete" onclick="deleteProduct(${prod.id})" data-permission="manage_products">Delete</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Failed to load products:', error);
    }
}

function showAddProduct() {
    document.getElementById('addProductModal').style.display = 'block';
    document.getElementById('productModalTitle').textContent = 'Add Product';
    document.getElementById('productForm').reset();
    document.getElementById('editProductId').value = '';
    document.getElementById('productSubmitBtn').textContent = 'Add Product';
}

function closeProductModal() {
    document.getElementById('addProductModal').style.display = 'none';
}

function editProduct(id) {
    const product = allProducts.find(p => p.id === id);
    if (!product) return;
    
    document.getElementById('addProductModal').style.display = 'block';
    document.getElementById('productModalTitle').textContent = 'Edit Product';
    document.getElementById('editProductId').value = product.id;
    document.getElementById('productName').value = product.name;
    document.getElementById('productPrice').value = product.price;
    document.getElementById('productDescription').value = product.description || '';
    document.getElementById('productQuantity').value = product.quantity || 1;
    document.getElementById('productQuantityUnit').value = product.quantity_unit || 'ML';
    document.getElementById('productSubmitBtn').textContent = 'Save';
}

async function deleteProduct(id) {
    if (confirm('Delete this product?')) {
        try {
            await API.products.delete(id);
            loadProducts();
        } catch (error) {
            alert('Failed to delete product');
        }
    }
}

document.getElementById('productForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const id = document.getElementById('editProductId').value;
    const data = {
        name: document.getElementById('productName').value,
        price: parseFloat(document.getElementById('productPrice').value),
        description: document.getElementById('productDescription').value,
        quantity: parseFloat(document.getElementById('productQuantity').value),
        quantity_unit: document.getElementById('productQuantityUnit').value,
        type: 'product'
    };
    
    try {
        if (id) {
            await API.products.update(id, data);
        } else {
            await API.products.create(data);
        }
        closeProductModal();
        loadProducts();
    } catch (error) {
        alert('Failed to save product');
    }
});

loadProducts();
