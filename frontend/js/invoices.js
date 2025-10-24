let locations = [];
let products = [];

async function loadInvoices() {
    try {
        const invoices = await API.invoices.getAll();
        const tbody = document.getElementById('invoiceTable');
        tbody.innerHTML = invoices.map(inv => `
            <tr>
                <td>${inv.id}</td>
                <td>${inv.invoice_number}</td>
                <td>${inv.customer_name}</td>
                <td>${new Date(inv.date).toLocaleDateString()}</td>
                <td>$${inv.total_amount.toFixed(2)}</td>
                <td><span class="badge-success">Completed</span></td>
                <td>
                    <button onclick="downloadPDF(${inv.id}, '${inv.invoice_number}')">Download PDF</button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Failed to load invoices:', error);
    }
}

async function loadFormData() {
    try {
        locations = await API.locations.getAll();
        products = await API.products.getAll();
        
        const baySelect = document.getElementById('bay');
        baySelect.innerHTML = locations.map(loc => 
            `<option value="${loc.id}">${loc.name}</option>`
        ).join('');
        
        const serviceSelect = document.getElementById('service');
        serviceSelect.innerHTML = products.map(prod => 
            `<option value="${prod.id}" data-price="${prod.price}">${prod.name} - $${prod.price}</option>`
        ).join('');
    } catch (error) {
        console.error('Failed to load form data:', error);
    }
}

function showCreateInvoice() {
    document.getElementById('createInvoiceModal').style.display = 'block';
    loadFormData();
}

function closeModal() {
    document.getElementById('createInvoiceModal').style.display = 'none';
}

function toggleInstallment() {
    const status = document.getElementById('status').value;
    document.getElementById('installmentGroup').style.display = 
        status === 'installment' ? 'block' : 'none';
}

document.getElementById('invoiceForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const customerName = document.getElementById('customerName').value;
    const locationId = parseInt(document.getElementById('bay').value);
    const serviceSelect = document.getElementById('service');
    const productId = parseInt(serviceSelect.value);
    const price = parseFloat(serviceSelect.options[serviceSelect.selectedIndex].dataset.price);
    
    const invoiceData = {
        customer_name: customerName,
        location_id: locationId,
        items: [{
            product_service_id: productId,
            quantity: 1,
            unit_price: price
        }]
    };
    
    try {
        await API.invoices.create(invoiceData);
        alert('Invoice created successfully!');
        closeModal();
        loadInvoices();
    } catch (error) {
        alert('Failed to create invoice: ' + error.message);
    }
});

function downloadPDF(id, invoiceNumber) {
    const token = getToken();
    const url = `http://localhost:8000/api/invoices/${id}/pdf`;
    
    fetch(url, {
        headers: { 'Authorization': `Bearer ${token}` }
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `invoice-${invoiceNumber}.pdf`;
        a.click();
    });
}

loadInvoices();
