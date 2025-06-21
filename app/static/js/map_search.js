// Map-based search functionality for Dream yours Real Estate
class MapSearch {
    constructor() {
        this.map = null;
        this.markers = [];
        this.activeMarker = null;
        this.boundaryLayer = null;
        this.isDrawingBoundary = false;
        this.searchBounds = null;
        this.properties = [];
        
        this.initializeMap();
        this.bindEvents();
        this.loadInitialProperties();
    }
    
    initializeMap() {
        // Fix Leaflet marker icon paths
        delete L.Icon.Default.prototype._getIconUrl;
        L.Icon.Default.mergeOptions({
            iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
            iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
        });

        // Initialize the map
        this.map = L.map('map').setView([39.8283, -98.5795], 4); // Center of USA

        // Add tile layer
        this.streetLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(this.map);
        
        // Add satellite layer (alternative)
        this.satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
            attribution: 'Tiles © Esri'
        });
        
        // Create layer control
        this.baseLayers = {
            "Street": this.streetLayer,
            "Satellite": this.satelliteLayer
        };
    }
    
    bindEvents() {
        // Search form events
        const searchForm = document.getElementById('search-form');
        const inputs = searchForm.querySelectorAll('input, select');
        
        let debounceTimer;
        inputs.forEach(input => {
            input.addEventListener('input', () => {
                clearTimeout(debounceTimer);
                debounceTimer = setTimeout(() => {
                    this.performSearch();
                }, 500);
            });
        });
        
        // Property list item clicks
        document.addEventListener('click', (e) => {
            const propertyItem = e.target.closest('.property-item');
            if (propertyItem) {
                this.selectProperty(propertyItem);
            }
        });
        
        // Map control buttons
        document.getElementById('zoom-to-fit').addEventListener('click', () => {
            this.zoomToFitMarkers();
        });
        
        document.getElementById('toggle-satellite').addEventListener('click', (e) => {
            this.toggleSatelliteView(e.target);
        });
        
        document.getElementById('draw-boundary').addEventListener('click', (e) => {
            this.toggleBoundaryDrawing(e.target);
        });
        
        document.getElementById('clear-boundary').addEventListener('click', () => {
            this.clearBoundary();
        });
        
        // Map click events for boundary drawing
        this.map.on('click', (e) => {
            if (this.isDrawingBoundary) {
                this.addBoundaryPoint(e.latlng);
            }
        });
    }
    
    loadInitialProperties() {
        // Load properties from the template data
        const propertyItems = document.querySelectorAll('.property-item');
        this.properties = Array.from(propertyItems).map(item => ({
            id: item.dataset.id,
            lat: parseFloat(item.dataset.lat),
            lng: parseFloat(item.dataset.lng),
            element: item
        })).filter(prop => prop.lat && prop.lng);
        
        this.updateMapMarkers();
        this.zoomToFitMarkers();
    }
    
    updateMapMarkers() {
        // Clear existing markers
        this.markers.forEach(marker => this.map.removeLayer(marker));
        this.markers = [];
        
        // Add new markers
        this.properties.forEach(property => {
            const marker = L.marker([property.lat, property.lng])
                .addTo(this.map)
                .on('click', () => {
                    this.selectPropertyById(property.id);
                });
            
            // Custom marker popup
            const propertyElement = property.element;
            const price = propertyElement.querySelector('.property-price').textContent;
            const details = propertyElement.querySelector('.property-details').textContent;
            const address = propertyElement.querySelector('.property-address').textContent;
            
            marker.bindPopup(`
                <div class="marker-popup">
                    <div class="popup-price">${price}</div>
                    <div class="popup-details">${details}</div>
                    <div class="popup-address">${address}</div>
                    <a href="/properties/${property.id}" class="popup-link">View Details</a>
                </div>
            `);
            
            this.markers.push(marker);
        });
    }
    
    selectProperty(propertyElement) {
        // Remove active class from all properties
        document.querySelectorAll('.property-item').forEach(item => {
            item.classList.remove('active');
        });
        
        // Add active class to selected property
        propertyElement.classList.add('active');
        
        // Find and highlight corresponding marker
        const propertyId = propertyElement.dataset.id;
        const lat = parseFloat(propertyElement.dataset.lat);
        const lng = parseFloat(propertyElement.dataset.lng);
        
        if (lat && lng) {
            // Pan to marker
            this.map.setView([lat, lng], Math.max(this.map.getZoom(), 15));
            
            // Find and open popup for the marker
            const marker = this.markers.find(m => {
                const markerLatLng = m.getLatLng();
                return Math.abs(markerLatLng.lat - lat) < 0.0001 && 
                       Math.abs(markerLatLng.lng - lng) < 0.0001;
            });
            
            if (marker) {
                marker.openPopup();
                this.activeMarker = marker;
            }
        }
    }
    
    selectPropertyById(propertyId) {
        const propertyElement = document.querySelector(`[data-id="${propertyId}"]`);
        if (propertyElement) {
            this.selectProperty(propertyElement);
            
            // Scroll property into view in sidebar
            propertyElement.scrollIntoView({
                behavior: 'smooth',
                block: 'center'
            });
        }
    }
    
    zoomToFitMarkers() {
        if (this.markers.length === 0) return;
        
        const group = new L.featureGroup(this.markers);
        this.map.fitBounds(group.getBounds().pad(0.1));
    }
    
    toggleSatelliteView(button) {
        if (this.map.hasLayer(this.streetLayer)) {
            this.map.removeLayer(this.streetLayer);
            this.map.addLayer(this.satelliteLayer);
            button.textContent = 'Street';
        } else {
            this.map.removeLayer(this.satelliteLayer);
            this.map.addLayer(this.streetLayer);
            button.textContent = 'Satellite';
        }
    }
    
    toggleBoundaryDrawing(button) {
        this.isDrawingBoundary = !this.isDrawingBoundary;
        
        if (this.isDrawingBoundary) {
            button.classList.add('active');
            button.textContent = 'Stop Drawing';
            this.map.getContainer().style.cursor = 'crosshair';
            
            // Clear existing boundary
            this.clearBoundary();
            
            // Initialize boundary points array
            this.boundaryPoints = [];
        } else {
            button.classList.remove('active');
            button.textContent = 'Draw Boundary';
            this.map.getContainer().style.cursor = '';
            
            // Complete the boundary if we have points
            if (this.boundaryPoints && this.boundaryPoints.length >= 3) {
                this.completeBoundary();
            }
        }
    }
    
    addBoundaryPoint(latlng) {
        if (!this.boundaryPoints) {
            this.boundaryPoints = [];
        }
        
        this.boundaryPoints.push(latlng);
        
        // Add a temporary marker
        const marker = L.circleMarker(latlng, {
            radius: 5,
            color: '#ff6b35',
            fillColor: '#ff6b35',
            fillOpacity: 0.8
        }).addTo(this.map);
        
        if (!this.tempMarkers) {
            this.tempMarkers = [];
        }
        this.tempMarkers.push(marker);
        
        // Draw lines between points
        if (this.boundaryPoints.length > 1) {
            const polyline = L.polyline(this.boundaryPoints, {
                color: '#ff6b35',
                weight: 2,
                dashArray: '5, 5'
            }).addTo(this.map);
            
            if (!this.tempLines) {
                this.tempLines = [];
            }
            this.tempLines.push(polyline);
        }
    }
    
    completeBoundary() {
        if (!this.boundaryPoints || this.boundaryPoints.length < 3) return;
        
        // Clear temporary markers and lines
        if (this.tempMarkers) {
            this.tempMarkers.forEach(marker => this.map.removeLayer(marker));
            this.tempMarkers = [];
        }
        if (this.tempLines) {
            this.tempLines.forEach(line => this.map.removeLayer(line));
            this.tempLines = [];
        }
        
        // Create the boundary polygon
        this.boundaryLayer = L.polygon(this.boundaryPoints, {
            color: '#006aff',
            weight: 2,
            fillColor: '#006aff',
            fillOpacity: 0.1
        }).addTo(this.map);
        
        // Set search bounds
        this.searchBounds = this.boundaryLayer.getBounds();
        
        // Filter properties within boundary
        this.filterPropertiesByBoundary();
    }
    
    clearBoundary() {
        if (this.boundaryLayer) {
            this.map.removeLayer(this.boundaryLayer);
            this.boundaryLayer = null;
        }
        
        if (this.tempMarkers) {
            this.tempMarkers.forEach(marker => this.map.removeLayer(marker));
            this.tempMarkers = [];
        }
        
        if (this.tempLines) {
            this.tempLines.forEach(line => this.map.removeLayer(line));
            this.tempLines = [];
        }
        
        this.searchBounds = null;
        this.boundaryPoints = [];
        
        // Reset drawing state
        this.isDrawingBoundary = false;
        const drawButton = document.getElementById('draw-boundary');
        drawButton.classList.remove('active');
        drawButton.textContent = 'Draw Boundary';
        this.map.getContainer().style.cursor = '';
        
        // Refresh search without boundary
        this.performSearch();
    }
    
    filterPropertiesByBoundary() {
        if (!this.searchBounds) return;
        
        // Filter properties that fall within the boundary
        const filteredProperties = this.properties.filter(property => {
            const point = L.latLng(property.lat, property.lng);
            return this.searchBounds.contains(point);
        });
        
        // Update the search with boundary coordinates
        this.performSearch(this.searchBounds);
    }
    
    performSearch(bounds = null) {
        const formData = new FormData(document.getElementById('search-form'));
        const params = new URLSearchParams();
        
        // Add form parameters
        for (let [key, value] of formData.entries()) {
            if (value.trim()) {
                params.append(key, value);
            }
        }
        
        // Add boundary parameters if exists
        if (bounds) {
            params.append('bounds', JSON.stringify({
                north: bounds.getNorth(),
                south: bounds.getSouth(),
                east: bounds.getEast(),
                west: bounds.getWest()
            }));
        }
        
        // Show loading indicator
        this.showLoading();
        
        // Make AJAX request
        fetch(`/api/map-search?${params.toString()}`)
            .then(response => response.json())
            .then(data => {
                this.updateSearchResults(data);
                this.hideLoading();
            })
            .catch(error => {
                console.error('Search error:', error);
                this.hideLoading();
            });
    }
    
    updateSearchResults(data) {
        // Update property list
        const propertyList = document.getElementById('property-list');
        propertyList.innerHTML = data.html;
        
        // Update results count
        document.getElementById('results-count').textContent = 
            `${data.results_count} of ${data.total_count} homes`;
        
        // Reload properties and update markers
        this.loadInitialProperties();
    }
    
    showLoading() {
        document.getElementById('loading-indicator').style.display = 'block';
    }
    
    hideLoading() {
        document.getElementById('loading-indicator').style.display = 'none';
    }
}

// Initialize map search when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    new MapSearch();
});

// Add custom popup styles
const style = document.createElement('style');
style.textContent = `
    .marker-popup {
        min-width: 200px;
    }
    .popup-price {
        font-size: 16px;
        font-weight: bold;
        color: #333;
        margin-bottom: 5px;
    }
    .popup-details {
        font-size: 12px;
        color: #666;
        margin-bottom: 5px;
    }
    .popup-address {
        font-size: 11px;
        color: #888;
        margin-bottom: 10px;
    }
    .popup-link {
        display: inline-block;
        background: #006aff;
        color: white;
        padding: 5px 10px;
        text-decoration: none;
        border-radius: 3px;
        font-size: 12px;
    }
    .popup-link:hover {
        background: #0056cc;
    }
`;
document.head.appendChild(style);
