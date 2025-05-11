document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registrationForm');

    // Set current date and time
    function formatDateTime() {
        const now = new Date();
        const date = now.getDate().toString().padStart(2, '0');
        const month = (now.getMonth() + 1).toString().padStart(2, '0');
        const year = now.getFullYear();
        const hours = now.getHours().toString().padStart(2, '0');
        const minutes = now.getMinutes().toString().padStart(2, '0');
        return `${date}/${month}/${year} ${hours}:${minutes}`;
    }
    
    // Set initial date/time and update every minute
    function updateDateTime() {
        document.getElementById('registrationDateTime').value = formatDateTime();
    }
    
    updateDateTime();
    setInterval(updateDateTime, 60000); // Update every minute

    // Get next patient code
    fetch('/api/patients/next-code')
        .then(response => response.json())
        .then(data => {
            document.getElementById('uniqueCode').value = data.next_code;
        });

    // Auto-set gender based on courtesy title
    document.getElementById('courtesyTitle').addEventListener('change', function() {
        const title = this.value;
        let gender = 'Other';
        if (['Mr.', 'Master', 'Shri.'].includes(title)) {
            gender = 'Male';
        } else if (['Mrs.', 'Ms.', 'Smt.', 'Baby-F'].includes(title)) {
            gender = 'Female';
        }
        document.getElementById('gender').value = gender;
    });

    // Handle doctor selection and auto-fill WhatsApp
    document.getElementById('referredBy').addEventListener('change', function() {
        const doctorName = this.value;
        fetch(`/api/doctors/${encodeURIComponent(doctorName)}`)
            .then(response => response.json())
            .then(data => {
                if (data.whatsapp_no) {
                    document.getElementById('doctorWhatsappNo').value = data.whatsapp_no;
                }
            });
    });

    // Form navigation with Enter key
    const formFields = [
        'courtesyTitle',
        'name',
        'age',
        'whatsappNo',
        'referredBy',
        'testCode',
        'discount',
        'paidAmount'
    ];

    formFields.forEach((fieldId, index) => {
        const element = document.getElementById(fieldId);
        if (element) {
            element.addEventListener('keypress', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    if (index < formFields.length - 1) {
                        document.getElementById(formFields[index + 1])?.focus();
                    }
                }
            });
        }
    });

    // Handle test code entry
    document.getElementById('testCode').addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            // Add test to table
            addTestToTable(this.value);
            this.value = '';  // Clear input
        }
    });

    // Update totals when tests or discounts change
    ['discount', 'paidAmount'].forEach(id => {
        document.getElementById(id)?.addEventListener('input', updateBalance);
    });

    // Calculate totals
    function updateTotals() {
        const total = calculateTotal();
        document.getElementById('totalAmount').value = total.toFixed(2);
        document.getElementById('paidAmount').value = total.toFixed(2);
        updateBalance();
    }

    function updateBalance() {
        const total = parseFloat(document.getElementById('totalAmount').value) || 0;
        const discount = parseFloat(document.getElementById('discount').value) || 0;
        const paid = parseFloat(document.getElementById('paidAmount').value) || 0;
        const balance = total - discount - paid;
        document.getElementById('balance').value = balance.toFixed(2);
    }

    function calculateTotal() {
        let total = 0;
        const testRows = document.querySelectorAll('#testTable tbody tr');
        testRows.forEach(row => {
            const price = parseFloat(row.querySelector('td:nth-child(3)').textContent) || 0;
            total += price;
        });
        return total;
    }

    function addTestToTable(testCode) {
        fetch(`/api/tests/${encodeURIComponent(testCode)}`)
            .then(response => response.json())
            .then(data => {
                if (data) {
                    const table = document.getElementById('testTable').getElementsByTagName('tbody')[0];
                    const newRow = table.insertRow(table.rows.length);

                    const testCodeCell = newRow.insertCell(0);
                    const testNameCell = newRow.insertCell(1);
                    const priceCell = newRow.insertCell(2);
                    const removeCell = newRow.insertCell(3);

                    testCodeCell.innerHTML = data.test_code;
                    testNameCell.innerHTML = data.test_name;
                    priceCell.innerHTML = data.price.toFixed(2);
                    removeCell.innerHTML = '<button onclick="removeTest(this)">Remove</button>';
                    updateTotals(); // Update totals after adding a test
                } else {
                    alert('Test code not found.');
                }
            });
    }

    function removeTest(btn) {
        const row = btn.parentNode.parentNode;
        row.parentNode.removeChild(row);
        updateTotals(); // Update totals after removing a test
    }
});