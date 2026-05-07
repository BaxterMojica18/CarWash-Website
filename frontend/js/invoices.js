let locations = [];
let products = [];
let allInvoices = [];
let filteredInvoices = [];
let invoicePage = 1;
const INVOICE_PAGE_SIZE = 10;

async function loadInvoices() {
    try {
        allInvoices = await API.invoices.getAll();
        filteredInvoices = allInvoices;
        
        // Check if navigated from dashboard with filter
        const savedFilter = localStorage.getItem('invoiceFilter');
        if (savedFilter) {
            document.getElementById('invoiceFilter').value = savedFilter;
            localStorage.removeItem('invoiceFilter');
            filterInvoices();
        } else {
            displayInvoices(allInvoices);
        }
    } catch (error) {
        console.error('Failed to load invoices:', error);
    }
}

function displayInvoices(invoices) {
    filteredInvoices = invoices;
    invoicePage = 1;
    renderInvoicePage();
}

function renderInvoicePage() {
    const tbody = document.getElementById('invoiceTable');
    const start = (invoicePage - 1) * INVOICE_PAGE_SIZE;
    const slice = filteredInvoices.slice(start, start + INVOICE_PAGE_SIZE);

    tbody.innerHTML = slice.map(inv => `
        <tr>
            <td>${inv.id}</td>
            <td>${inv.invoice_number}</td>
            <td>${inv.customer_name}</td>
            <td>${new Date(inv.date).toLocaleDateString()}</td>
            <td>$${inv.total_amount.toFixed(2)}</td>
            <td><span class="badge-success">Completed</span></td>
            <td>
                <button onclick="downloadPDF(${inv.id}, '${inv.invoice_number}')" style="background: var(--sidebar-color, #2c3e50); color: white; border: none; padding: 6px 12px; border-radius: 5px; cursor: pointer; margin-right: 5px; font-size: 12px;">PDF</button>
                <button class="btn-secondary" style="padding: 6px 12px; font-size: 12px;" onclick="downloadJPG(${inv.id}, '${inv.invoice_number}')">JPG</button>
            </td>
        </tr>
    `).join('');

    const totalPages = Math.ceil(filteredInvoices.length / INVOICE_PAGE_SIZE);
    let bar = document.getElementById('invoicePagination');
    if (!bar) return;
    bar.innerHTML = '';
    if (totalPages <= 1) return;

    const prev = document.createElement('button');
    prev.textContent = '‹';
    prev.className = 'page-btn';
    prev.disabled = invoicePage === 1;
    prev.onclick = () => { invoicePage--; renderInvoicePage(); };
    bar.appendChild(prev);

    for (let i = 1; i <= totalPages; i++) {
        const btn = document.createElement('button');
        btn.textContent = i;
        btn.className = 'page-btn' + (i === invoicePage ? ' active' : '');
        btn.onclick = ((p) => () => { invoicePage = p; renderInvoicePage(); })(i);
        bar.appendChild(btn);
    }

    const next = document.createElement('button');
    next.textContent = '›';
    next.className = 'page-btn';
    next.disabled = invoicePage === totalPages;
    next.onclick = () => { invoicePage++; renderInvoicePage(); };
    bar.appendChild(next);
}

function filterInvoices() {
    const period = document.getElementById('invoiceFilter').value;
    const now = new Date();
    let startDate = new Date();
    
    if (period === 'all') {
        filteredInvoices = allInvoices;
    } else {
        switch(period) {
            case 'weekly':
                startDate.setDate(now.getDate() - 7);
                break;
            case 'monthly':
                startDate.setMonth(now.getMonth() - 1);
                break;
            case 'quarterly':
                startDate.setMonth(now.getMonth() - 3);
                break;
            case 'annually':
                startDate.setFullYear(now.getFullYear() - 1);
                break;
        }
        
        filteredInvoices = allInvoices.filter(inv => {
            const invDate = new Date(inv.date);
            return invDate >= startDate && invDate <= now;
        });
    }
    
    searchInvoices();
}

function searchInvoices() {
    const searchTerm = document.getElementById('searchInvoice').value.toLowerCase();
    const filtered = filteredInvoices.filter(inv => 
        inv.invoice_number.toLowerCase().includes(searchTerm) ||
        inv.customer_name.toLowerCase().includes(searchTerm)
    );
    displayInvoices(filtered);
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
    const token = localStorage.getItem('token');
    const url = `${API_BASE}/invoices/${id}/pdf`;
    
    fetch(url, {
        headers: { 'Authorization': `Bearer ${token}` }
    })
    .then(response => {
        if (!response.ok) throw new Error('Download failed');
        return response.blob();
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `invoice-${invoiceNumber}.pdf`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    })
    .catch(error => {
        console.error('PDF download error:', error);
        alert('Failed to download PDF');
    });
}

async function downloadJPG(id, invoiceNumber) {
    const token = localStorage.getItem('token');
    const url = `${API_BASE}/invoices/${id}/jpg?token=${token}`;
    
    fetch(url)
    .then(response => {
        if (!response.ok) throw new Error('Download failed');
        return response.blob();
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `invoice-${invoiceNumber}.jpg`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    })
    .catch(error => {
        console.error('JPG download error:', error);
        alert('Failed to download JPG');
    });
}

loadInvoices();
