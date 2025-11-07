async function loadServices() {
    try {
        const products = await API.products.getAll();
        const servicesList = products.filter(p => p.type === 'service');
        
        const grid = document.getElementById('servicesGrid');
        grid.innerHTML = servicesList.map(service => `
            <div class="product-card">
                <h3>${service.name}</h3>
                <p class="price">$${service.price.toFixed(2)}</p>
                <p>${service.description || ''}</p>
                <div class="product-actions">
                    <button class="btn-edit" onclick='editService(${JSON.stringify(service)})' data-permission="manage_products">Edit</button>
                    <button class="btn-delete" onclick="deleteService(${service.id})" data-permission="manage_products">Delete</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Failed to load services:', error);
    }
}

function showAddService() {
    document.getElementById('addServiceModal').style.display = 'block';
    document.getElementById('serviceModalTitle').textContent = 'Add Service';
    document.getElementById('serviceForm').reset();
    document.getElementById('editServiceId').value = '';
}

function closeServiceModal() {
    document.getElementById('addServiceModal').style.display = 'none';
}

function editService(service) {
    document.getElementById('addServiceModal').style.display = 'block';
    document.getElementById('serviceModalTitle').textContent = 'Edit Service';
    document.getElementById('editServiceId').value = service.id;
    document.getElementById('serviceName').value = service.name;
    document.getElementById('servicePrice').value = service.price;
    document.getElementById('serviceDescription').value = service.description || '';
}

async function deleteService(id) {
    if (confirm('Delete this service?')) {
        try {
            await API.products.delete(id);
            loadServices();
        } catch (error) {
            alert('Failed to delete service');
        }
    }
}

document.getElementById('serviceForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const id = document.getElementById('editServiceId').value;
    const data = {
        name: document.getElementById('serviceName').value,
        price: parseFloat(document.getElementById('servicePrice').value),
        description: document.getElementById('serviceDescription').value,
        type: 'service'
    };
    
    try {
        if (id) {
            await API.products.update(id, data);
        } else {
            await API.products.create(data);
        }
        closeServiceModal();
        loadServices();
    } catch (error) {
        alert('Failed to save service');
    }
});

loadServices();
