async function loadProducts() {
    try {
        const products = await API.products.getAll();
        const grid = document.getElementById('productsGrid');
        grid.innerHTML = products.map(prod => `
            <div class="product-card">
                <h3>${prod.name}</h3>
                <p class="price">$${prod.price.toFixed(2)}</p>
                <p>${prod.description || ''}</p>
                <span class="badge">${prod.type}</span>
                <div class="product-actions">
                    <button onclick='editProduct(${JSON.stringify(prod)})'>Edit</button>
                    <button onclick="deleteProduct(${prod.id})">Delete</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Failed to load products:', error);
    }
}

function showAddProduct() {
    document.getElementById('addProductModal').style.display = 'block';
    document.getElementById('productModalTitle').textContent = 'Add Product/Service';
    document.getElementById('productForm').reset();
    document.getElementById('editProductId').value = '';
}

function closeProductModal() {
    document.getElementById('addProductModal').style.display = 'none';
}

function editProduct(product) {
    document.getElementById('addProductModal').style.display = 'block';
    document.getElementById('productModalTitle').textContent = 'Edit Product/Service';
    document.getElementById('editProductId').value = product.id;
    document.getElementById('productName').value = product.name;
    document.getElementById('productPrice').value = product.price;
    document.getElementById('productDescription').value = product.description || '';
}

async function deleteProduct(id) {
    if (confirm('Delete this product/service?')) {
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
        type: 'service'
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
