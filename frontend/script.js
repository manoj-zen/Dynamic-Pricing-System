// Configuration
const API_BASE_URL = localStorage.getItem('apiUrl') || 'http://localhost:5000';
let currentPage = 0;
const itemsPerPage = 20;
let allProducts = [];

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
    setupTabs();
    initializeEventListeners();
    await checkAPIStatus();
    loadDashboardData();
});

// Setup Tabs
function setupTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabName = button.getAttribute('data-tab');
            
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            button.classList.add('active');
            document.getElementById(tabName).classList.add('active');
        });
    });
}

// Event Listeners
function initializeEventListeners() {
    document.getElementById('product-search').addEventListener('input', searchProducts);
    document.getElementById('sort-by').addEventListener('change', sortProducts);
}

// API Calls
async function apiCall(endpoint, method = 'GET', data = null) {
    try {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
            }
        };

        if (data) {
            options.body = JSON.stringify(data);
        }

        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        
        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        showToast(`Error: ${error.message}`, 'error');
        console.error('API Call Error:', error);
        return null;
    }
}

async function checkAPIStatus() {
    const result = await apiCall('/health');
    const statusBadge = document.getElementById('status');
    
    if (result) {
        statusBadge.textContent = '🟢 Online';
        statusBadge.classList.add('active');
        document.getElementById('api-status').textContent = 'Active';
    } else {
        statusBadge.textContent = '🔴 Offline';
        statusBadge.classList.add('error');
        document.getElementById('api-status').textContent = 'Offline';
    }
}

// Dashboard
async function loadDashboardData() {
    const health = await apiCall('/health');
    const modelStatus = await apiCall('/model-status');

    if (health) {
        document.getElementById('total-products').textContent = health.products_loaded;
    }

    if (modelStatus) {
        document.getElementById('model-status').textContent = modelStatus.status === 'loaded' ? 'Ready' : 'Not Loaded';
    }

    loadInfoPanel();
}

async function loadInfoPanel() {
    const health = await apiCall('/health');
    const modelStatus = await apiCall('/model-status');
    
    let infoHtml = '';
    
    if (health) {
        infoHtml += `
            <div class="info-box-item">
                <span class="info-box-label">Total Products:</span>
                <span class="info-box-value">${health.products_loaded}</span>
            </div>
            <div class="info-box-item">
                <span class="info-box-label">Model Loaded:</span>
                <span class="info-box-value">${health.model_loaded ? 'Yes' : 'No'}</span>
            </div>
        `;
    }
    
    if (modelStatus && modelStatus.status === 'loaded') {
        infoHtml += `
            <div class="info-box-item">
                <span class="info-box-label">Model Type:</span>
                <span class="info-box-value">${modelStatus.model_type}</span>
            </div>
            <div class="info-box-item">
                <span class="info-box-label">Features:</span>
                <span class="info-box-value">${modelStatus.features.length}</span>
            </div>
        `;
    }
    
    infoHtml += `
        <div class="info-box-item">
            <span class="info-box-label">API Base URL:</span>
            <span class="info-box-value">${API_BASE_URL}</span>
        </div>
        <div class="info-box-item">
            <span class="info-box-label">Last Updated:</span>
            <span class="info-box-value">${new Date().toLocaleTimeString()}</span>
        </div>
    `;
    
    document.getElementById('info-panel').innerHTML = infoHtml;
}

function refreshDashboard() {
    loadDashboardData();
    showToast('Dashboard refreshed', 'success');
}

// Products
async function loadAllProducts() {
    const result = await apiCall(`/products?skip=0&limit=500`);
    if (result) {
        allProducts = result.products;
        currentPage = 0;
        displayProducts();
        showToast(`Loaded ${allProducts.length} products`, 'success');
    }
}

function displayProducts() {
    const start = currentPage * itemsPerPage;
    const end = start + itemsPerPage;
    const pageProducts = allProducts.slice(start, end);

    let html = '';
    pageProducts.forEach(product => {
        html += `
            <div class="product-card">
                <h4>${product.name}</h4>
                <div class="product-info">
                    <strong>Price:</strong> ₹${product.base_price}
                </div>
                <div class="product-info">
                    <strong>Stock:</strong> ${product.stock} units
                </div>
                <div class="product-info">
                    <strong>7-Day Sales:</strong> ${product.sales_7}
                </div>
                <div class="product-info">
                    <strong>30-Day Sales:</strong> ${product.sales_30}
                </div>
                <button class="btn btn-primary" onclick="getPriceForProduct(${product.product_id})">
                    Get Dynamic Price
                </button>
            </div>
        `;
    });

    document.getElementById('products-list').innerHTML = html;
    document.getElementById('page-info').textContent = `Page ${currentPage + 1} of ${Math.ceil(allProducts.length / itemsPerPage)}`;
}

function nextPage() {
    const maxPage = Math.ceil(allProducts.length / itemsPerPage) - 1;
    if (currentPage < maxPage) {
        currentPage++;
        displayProducts();
        window.scrollTo(0, 0);
    }
}

function previousPage() {
    if (currentPage > 0) {
        currentPage--;
        displayProducts();
        window.scrollTo(0, 0);
    }
}

function searchProducts() {
    const searchTerm = document.getElementById('product-search').value.toLowerCase();
    const filtered = allProducts.filter(p => 
        p.name.toLowerCase().includes(searchTerm)
    );
    
    currentPage = 0;
    allProducts = filtered;
    displayProducts();
}

function sortProducts() {
    const sortBy = document.getElementById('sort-by').value;
    
    switch(sortBy) {
        case 'name':
            allProducts.sort((a, b) => a.name.localeCompare(b.name));
            break;
        case 'price':
            allProducts.sort((a, b) => a.base_price - b.base_price);
            break;
        case 'stock':
            allProducts.sort((a, b) => a.stock - b.stock);
            break;
        case 'demand':
            allProducts.sort((a, b) => b.sales_7 - a.sales_7);
            break;
    }
    
    currentPage = 0;
    displayProducts();
}

// Pricing
async function getPriceForProduct(productId) {
    const result = await apiCall(`/price/${productId}`);
    if (result) {
        displayPricingResult(result);
    }
}

async function calculatePrice() {
    const productId = parseInt(document.getElementById('calc-product-id').value);
    const basePrice = parseFloat(document.getElementById('calc-base-price').value);
    const stock = parseInt(document.getElementById('calc-stock').value);
    const sales7 = parseInt(document.getElementById('calc-sales-7').value);
    const sales30 = parseInt(document.getElementById('calc-sales-30').value);
    const day = parseInt(document.getElementById('calc-day').value);

    if (!productId || !basePrice || stock < 0 || sales7 < 0 || sales30 < 0) {
        showToast('Please fill all fields correctly', 'error');
        return;
    }

    const result = await apiCall('/predict-price', 'POST', {
        product_id: productId,
        base_price: basePrice,
        stock,
        sales_7: sales7,
        sales_30: sales30,
        day
    });

    if (result) {
        displayPricingResult(result);
    }
}

function displayPricingResult(result) {
    let html = `
        <div class="result-item">
            <div class="result-item-label">Base Price</div>
            <div class="result-item-value">₹${result.base_price.toFixed(2)}</div>
        </div>
        <div class="result-item">
            <div class="result-item-label">Price Multiplier</div>
            <div class="result-item-value">${result.multiplier}x</div>
        </div>
        <div class="result-item">
            <div class="result-item-label">Dynamic Price</div>
            <div class="result-item-value">₹${result.dynamic_price.toFixed(2)}</div>
        </div>
        <div class="result-item">
            <div class="result-item-label">Change</div>
            <div class="result-item-value" style="color: ${result.change_percent > 0 ? '#10b981' : '#ef4444'}">
                ${result.change_percent > 0 ? '+' : ''}${result.change_percent}%
            </div>
        </div>
        <div class="result-recommendation">
            📌 ${result.recommendation}
        </div>
    `;

    const resultBox = document.getElementById('pricing-result');
    resultBox.querySelector('.result-content').innerHTML = html;
    resultBox.style.display = 'block';
}

// Model Training
async function trainModel() {
    const statusBadge = document.getElementById('status');
    statusBadge.textContent = 'Training...';
    statusBadge.classList.remove('active', 'error');
    statusBadge.classList.add('loading');

    const result = await apiCall('/train-model', 'POST');

    if (result) {
        statusBadge.textContent = '🟢 Online';
        statusBadge.classList.remove('loading');
        statusBadge.classList.add('active');
        
        showToast(`✅ Model trained successfully!\nTrain Score: ${(result.train_score * 100).toFixed(2)}%\nTest Score: ${(result.test_score * 100).toFixed(2)}%`, 'success');
        loadDashboardData();
    } else {
        statusBadge.textContent = '🔴 Error';
        statusBadge.classList.remove('loading');
        statusBadge.classList.add('error');
    }
}

// Analytics
async function loadAnalytics() {
    const topDemand = await apiCall('/analytics/top-demand?limit=10');
    const lowStock = await apiCall('/analytics/low-stock?threshold=10');
    const highValue = await apiCall('/analytics/high-value?limit=10');

    if (topDemand) {
        displayTopDemand(topDemand.top_products);
    }
    if (lowStock) {
        displayLowStock(lowStock.low_stock_products);
    }
    if (highValue) {
        displayHighValue(highValue.high_value_products);
    }
}

function displayTopDemand(products) {
    let html = '<table><thead><tr><th>Product</th><th>7-Day Sales</th><th>30-Day Sales</th></tr></thead><tbody>';
    products.forEach(p => {
        html += `<tr><td>${p.name}</td><td>${p.sales_7}</td><td>${p.sales_30}</td></tr>`;
    });
    html += '</tbody></table>';
    document.getElementById('top-demand').innerHTML = html;
}

function displayLowStock(products) {
    let html = '<table><thead><tr><th>Product</th><th>Stock</th><th>7-Day Sales</th></tr></thead><tbody>';
    products.forEach(p => {
        html += `<tr><td>${p.name}</td><td>${p.stock}</td><td>${p.sales_7}</td></tr>`;
    });
    html += '</tbody></table>';
    document.getElementById('low-stock').innerHTML = html;
}

function displayHighValue(products) {
    let html = '<table><thead><tr><th>Product</th><th>Price</th><th>Stock</th></tr></thead><tbody>';
    products.forEach(p => {
        html += `<tr><td>${p.name}</td><td>₹${p.base_price}</td><td>${p.stock}</td></tr>`;
    });
    html += '</tbody></table>';
    document.getElementById('high-value').innerHTML = html;
}

// Settings
function saveApiUrl() {
    const url = document.getElementById('api-url').value;
    localStorage.setItem('apiUrl', url);
    location.reload();
}

function exportData() {
    if (allProducts.length === 0) {
        showToast('No products loaded. Click "Load Products" first.', 'error');
        return;
    }

    const csv = convertToCSV(allProducts);
    downloadCSV(csv, 'products.csv');
    showToast('Products exported successfully', 'success');
}

function convertToCSV(data) {
    const headers = Object.keys(data[0]);
    let csv = headers.join(',') + '\n';
    
    data.forEach(row => {
        csv += headers.map(header => {
            const value = row[header];
            return typeof value === 'string' ? `"${value}"` : value;
        }).join(',') + '\n';
    });
    
    return csv;
}

function downloadCSV(csv, filename) {
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

// Toast Notification
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast show ${type}`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Monitor tab visibility to load analytics when switching
const observer = new MutationObserver(() => {
    const analyticsTab = document.getElementById('analytics');
    if (analyticsTab && analyticsTab.classList.contains('active')) {
        loadAnalytics();
    }
});

observer.observe(document.querySelector('.tabs'), { 
    subtree: true, 
    attributes: true, 
    attributeFilter: ['class'] 
});
