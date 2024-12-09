// Table sorting and filtering utilities
function setupTableSorting(tableId) {
    const table = document.getElementById(tableId);
    if (!table) return;

    const headers = table.querySelectorAll('th');
    headers.forEach((header, index) => {
        if (header.classList.contains('no-sort')) return;

        header.style.cursor = 'pointer';
        header.addEventListener('click', () => sortTable(table, index));
        
        // Add sort indicators
        const indicator = document.createElement('span');
        indicator.className = 'sort-indicator ms-1';
        indicator.innerHTML = '↕️';
        header.appendChild(indicator);
    });
}

function sortTable(table, column) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const headers = table.querySelectorAll('th');
    const currentHeader = headers[column];
    
    // Toggle sort direction
    const isAscending = currentHeader.getAttribute('data-sort') !== 'asc';
    headers.forEach(h => h.setAttribute('data-sort', ''));
    currentHeader.setAttribute('data-sort', isAscending ? 'asc' : 'desc');
    
    // Update sort indicators
    headers.forEach(header => {
        const indicator = header.querySelector('.sort-indicator');
        if (indicator) {
            indicator.innerHTML = '↕️';
        }
    });
    const currentIndicator = currentHeader.querySelector('.sort-indicator');
    if (currentIndicator) {
        currentIndicator.innerHTML = isAscending ? '↑' : '↓';
    }

    // Sort rows
    rows.sort((a, b) => {
        const aValue = a.cells[column].textContent.trim();
        const bValue = b.cells[column].textContent.trim();
        
        // Check if the values are dates
        const aDate = new Date(aValue);
        const bDate = new Date(bValue);
        if (!isNaN(aDate) && !isNaN(bDate)) {
            return isAscending ? aDate - bDate : bDate - aDate;
        }
        
        // Check if the values are numbers
        const aNum = parseFloat(aValue);
        const bNum = parseFloat(bValue);
        if (!isNaN(aNum) && !isNaN(bNum)) {
            return isAscending ? aNum - bNum : bNum - aNum;
        }
        
        // Sort as strings
        return isAscending ? 
            aValue.localeCompare(bValue, 'es') : 
            bValue.localeCompare(aValue, 'es');
    });

    // Reorder table rows
    rows.forEach(row => tbody.appendChild(row));
}

function setupAdvancedFilter(tableId, filters) {
    const table = document.getElementById(tableId);
    if (!table) return;

    const filterContainer = document.createElement('div');
    filterContainer.className = 'mb-3';
    
    // Create filter controls
    filters.forEach(filter => {
        const filterGroup = document.createElement('div');
        filterGroup.className = 'mb-2';
        
        const label = document.createElement('label');
        label.className = 'me-2';
        label.textContent = filter.label + ':';
        filterGroup.appendChild(label);

        if (filter.type === 'select') {
            const select = document.createElement('select');
            select.className = 'form-select form-select-sm d-inline-block w-auto';
            select.setAttribute('data-column', filter.column);
            
            const defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.textContent = 'Todos';
            select.appendChild(defaultOption);

            // Get unique values from column
            const values = new Set();
            table.querySelectorAll(`tbody tr td:nth-child(${filter.column + 1})`).forEach(cell => {
                values.add(cell.textContent.trim());
            });

            Array.from(values).sort().forEach(value => {
                const option = document.createElement('option');
                option.value = value;
                option.textContent = value;
                select.appendChild(option);
            });

            select.addEventListener('change', () => applyFilters(table));
            filterGroup.appendChild(select);
        } else if (filter.type === 'date') {
            const dateInput = document.createElement('input');
            dateInput.type = 'date';
            dateInput.className = 'form-control form-control-sm d-inline-block w-auto';
            dateInput.setAttribute('data-column', filter.column);
            dateInput.addEventListener('change', () => applyFilters(table));
            filterGroup.appendChild(dateInput);
        }

        filterContainer.appendChild(filterGroup);
    });

    // Add filter container before table
    table.parentNode.insertBefore(filterContainer, table);
}

function applyFilters(table) {
    const rows = table.querySelectorAll('tbody tr');
    const filters = table.parentNode.querySelectorAll('select, input[type="date"]');

    rows.forEach(row => {
        let show = true;

        filters.forEach(filter => {
            const value = filter.value.toLowerCase();
            if (!value) return;

            const column = parseInt(filter.getAttribute('data-column'));
            const cellValue = row.cells[column].textContent.trim().toLowerCase();

            if (filter.type === 'date') {
                const cellDate = new Date(cellValue);
                const filterDate = new Date(value);
                if (cellDate.toDateString() !== filterDate.toDateString()) {
                    show = false;
                }
            } else if (!cellValue.includes(value)) {
                show = false;
            }
        });

        row.style.display = show ? '' : 'none';
    });
}