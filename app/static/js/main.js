document.addEventListener("DOMContentLoaded", function() {
    console.log("CityPulse AI: Core System Initialized.");
    
    // Initialize Leaflet Map if the container exists on the page
    const mapContainer = document.getElementById('cityMap');
    if (mapContainer) {
        initMap();
    }
});

/**
 * Initializes the Leaflet GIS Map and fetches user's current GPS location.
 */
function initMap() {
    // Default location (Center of city, fallback if GPS is denied)
    let defaultLat = 19.9975; 
    let defaultLng = 73.7898;
    
    const map = L.map('cityMap').setView([defaultLat, defaultLng], 13);
    
    // Load OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    let userMarker = null;

    // Try to get actual GPS coordinates
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const lat = position.coords.latitude;
                const lng = position.coords.longitude;
                
                // Update map view
                map.setView([lat, lng], 16);
                
                // Place marker
                userMarker = L.marker([lat, lng], {draggable: true}).addTo(map)
                    .bindPopup("<b>Issue Location</b><br>Drag to adjust.").openPopup();
                
                // Update hidden form fields for Backend
                updateFormCoordinates(lat, lng);

                // Listen for drag events to refine location
                userMarker.on('dragend', function(event) {
                    const marker = event.target;
                    const position = marker.getLatLng();
                    updateFormCoordinates(position.lat, position.lng);
                });
            },
            (error) => {
                console.warn("GPS Access denied or unavailable. Using default map center.");
            }
        );
    } else {
        console.error("Geolocation is not supported by this browser.");
    }
}

/**
 * Populates hidden form inputs so the Flask backend receives the exact location.
 */
function updateFormCoordinates(lat, lng) {
    const latInput = document.getElementById('latitude');
    const lngInput = document.getElementById('longitude');
    
    if(latInput && lngInput) {
        latInput.value = lat;
        lngInput.value = lng;
    }
}