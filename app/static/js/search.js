// Enhanced search functionality for Dream yours Real Estate
document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.querySelector('.search-form');
    const homeSearchForm = document.querySelector('.search-bar-container');
    
    // Auto-submit search form on input change (with debounce)
    if (searchForm) {
        const inputs = searchForm.querySelectorAll('input, select');
        let debounceTimer;
        
        inputs.forEach(input => {
            input.addEventListener('input', function() {
                clearTimeout(debounceTimer);
                debounceTimer = setTimeout(() => {
                    // Only auto-submit if there's a search query
                    const searchQuery = document.getElementById('q').value;
                    if (searchQuery.length >= 2) {
                        performAjaxSearch();
                    }
                }, 500); // 500ms debounce
            });
        });
    }
    
    // Handle home page search
    if (homeSearchForm) {
        homeSearchForm.addEventListener('submit', function(e) {
            const searchInput = this.querySelector('input[name="q"]');
            if (!searchInput.value.trim()) {
                e.preventDefault();
                alert('Please enter a search term');
                return false;
            }
        });
    }
    
    // AJAX search function
    function performAjaxSearch() {
        const formData = new FormData(searchForm);
        const params = new URLSearchParams();
        
        // Build query parameters
        for (let [key, value] of formData.entries()) {
            if (value.trim()) {
                params.append(key, value);
            }
        }
        
        // Show loading indicator
        showLoadingIndicator();
        
        // Make AJAX request
        fetch(`/api/search?${params.toString()}`)
            .then(response => response.json())
            .then(data => {
                updateSearchResults(data);
                hideLoadingIndicator();
            })
            .catch(error => {
                console.error('Search error:', error);
                hideLoadingIndicator();
                showErrorMessage('Search failed. Please try again.');
            });
    }
    
    // Update search results without page reload
    function updateSearchResults(data) {
        const resultsContainer = document.querySelector('.property-grid');
        const resultsHeader = document.querySelector('.results-header p');
        
        if (!resultsContainer) return;
        
        // Update results count
        if (resultsHeader) {
            resultsHeader.textContent = `Found ${data.count} properties`;
        }
        
        // Clear existing results
        resultsContainer.innerHTML = '';
        
        if (data.properties.length === 0) {
            resultsContainer.innerHTML = `
                <div class="no-results" style="grid-column: 1 / -1;">
                    <h3>No properties found</h3>
                    <p>Try adjusting your search criteria or <a href="/search">clear all filters</a> to see all properties.</p>
                </div>
            `;
            return;
        }
        
        // Add new results
        data.properties.forEach(property => {
            const propertyCard = createPropertyCard(property);
            resultsContainer.appendChild(propertyCard);
        });
    }
    
    // Create property card element
    function createPropertyCard(property) {
        const card = document.createElement('div');
        card.className = 'property-card';
        
        const photoUrl = property.photo_url || '/static/images/placeholder-home.jpg';
        const price = new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(property.price);
        
        const sqft = new Intl.NumberFormat('en-US').format(property.sqft);
        
        card.innerHTML = `
            <a href="/properties/${property.id}">
                <img src="${photoUrl}" alt="Property image" loading="lazy">
                <div class="property-info">
                    <h3>${escapeHtml(property.title)}</h3>
                    <p class="price">${price}</p>
                    <p class="details">${property.bedrooms} beds | ${property.bathrooms} baths | ${sqft} sqft</p>
                    <p class="location">${escapeHtml(property.address)}</p>
                    <p class="location">${escapeHtml(property.city)}, ${escapeHtml(property.state)} ${escapeHtml(property.zip_code)}</p>
                </div>
            </a>
        `;
        
        return card;
    }
    
    // Utility functions
    function showLoadingIndicator() {
        const indicator = document.getElementById('loading-indicator');
        if (!indicator) {
            const loader = document.createElement('div');
            loader.id = 'loading-indicator';
            loader.innerHTML = `
                <div style="text-align: center; padding: 20px;">
                    <div style="display: inline-block; width: 20px; height: 20px; border: 3px solid #f3f3f3; border-top: 3px solid #0074E4; border-radius: 50%; animation: spin 1s linear infinite;"></div>
                    <p style="margin-top: 10px; color: #666;">Searching properties...</p>
                </div>
            `;
            
            const resultsContainer = document.querySelector('.search-results');
            if (resultsContainer) {
                resultsContainer.appendChild(loader);
            }
        } else {
            indicator.style.display = 'block';
        }
        
        // Add CSS animation if not exists
        if (!document.getElementById('spinner-style')) {
            const style = document.createElement('style');
            style.id = 'spinner-style';
            style.textContent = `
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
            `;
            document.head.appendChild(style);
        }
    }
    
    function hideLoadingIndicator() {
        const indicator = document.getElementById('loading-indicator');
        if (indicator) {
            indicator.style.display = 'none';
        }
    }
    
    function showErrorMessage(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.style.cssText = `
            background-color: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            border: 1px solid #f5c6cb;
        `;
        errorDiv.textContent = message;
        
        const resultsContainer = document.querySelector('.search-results');
        if (resultsContainer) {
            resultsContainer.insertBefore(errorDiv, resultsContainer.firstChild);
            
            // Remove error message after 5 seconds
            setTimeout(() => {
                errorDiv.remove();
            }, 5000);
        }
    }
    
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // Price range slider functionality (if implemented)
    const priceInputs = document.querySelectorAll('#min_price, #max_price');
    priceInputs.forEach(input => {
        input.addEventListener('input', function() {
            // Format price display
            if (this.value) {
                const formatted = new Intl.NumberFormat('en-US', {
                    style: 'currency',
                    currency: 'USD',
                    minimumFractionDigits: 0,
                    maximumFractionDigits: 0
                }).format(this.value);
                
                // Update placeholder or label if needed
                const label = document.querySelector(`label[for="${this.id}"]`);
                if (label && this.value) {
                    label.textContent = `${label.textContent.split(' (')[0]} (${formatted})`;
                }
            }
        });
    });
    
    // Clear filters functionality
    const clearBtn = document.querySelector('.clear-btn');
    if (clearBtn) {
        clearBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Clear all form inputs
            const form = document.querySelector('.search-form');
            if (form) {
                form.reset();
                
                // Trigger search with empty parameters
                window.location.href = '/search';
            }
        });
    }
});

// Global function to handle quick searches from anywhere
function quickSearch(query) {
    window.location.href = `/search?q=${encodeURIComponent(query)}`;
}

// Add search suggestions functionality (future enhancement)
function initSearchSuggestions() {
    const searchInput = document.getElementById('q');
    if (!searchInput) return;
    
    let suggestionsContainer;
    
    searchInput.addEventListener('input', function() {
        const query = this.value.trim();
        
        if (query.length >= 2) {
            // Create suggestions container if it doesn't exist
            if (!suggestionsContainer) {
                suggestionsContainer = document.createElement('div');
                suggestionsContainer.className = 'search-suggestions';
                suggestionsContainer.style.cssText = `
                    position: absolute;
                    top: 100%;
                    left: 0;
                    right: 0;
                    background: white;
                    border: 1px solid #ddd;
                    border-top: none;
                    border-radius: 0 0 5px 5px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    z-index: 1000;
                    max-height: 200px;
                    overflow-y: auto;
                `;
                
                this.parentNode.style.position = 'relative';
                this.parentNode.appendChild(suggestionsContainer);
            }
            
            // Here you could fetch suggestions from an API
            // For now, we'll show some static suggestions
            const suggestions = [
                'Springfield, IL',
                'Riverside, CA',
                'Beverly Hills, CA',
                'Austin, TX',
                'Miami, FL'
            ].filter(s => s.toLowerCase().includes(query.toLowerCase()));
            
            if (suggestions.length > 0) {
                suggestionsContainer.innerHTML = suggestions.map(suggestion => 
                    `<div class="suggestion-item" style="padding: 10px; cursor: pointer; border-bottom: 1px solid #eee;" onclick="quickSearch('${suggestion}')">${suggestion}</div>`
                ).join('');
                suggestionsContainer.style.display = 'block';
            } else {
                suggestionsContainer.style.display = 'none';
            }
        } else if (suggestionsContainer) {
            suggestionsContainer.style.display = 'none';
        }
    });
    
    // Hide suggestions when clicking outside
    document.addEventListener('click', function(e) {
        if (suggestionsContainer && !searchInput.contains(e.target) && !suggestionsContainer.contains(e.target)) {
            suggestionsContainer.style.display = 'none';
        }
    });
}

// Initialize search suggestions when DOM is ready
document.addEventListener('DOMContentLoaded', initSearchSuggestions);
