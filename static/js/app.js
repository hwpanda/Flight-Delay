document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const banner = document.getElementById('prediction-banner');
    const featuresBody = document.getElementById('features-table-body');
    const airportInputs = [
        document.getElementById('origin-airport'),
        document.getElementById('dest-airport'),
    ];
    const supportedAirportCodes = new Set(
        Array.from(
            document.querySelectorAll('#supported-airports option'),
            (option) => option.value,
        ),
    );
    let map;
    let routeLayer;

    function validateAirportInput(input) {
        input.value = input.value.toUpperCase();
        const code = input.value.trim();
        input.setCustomValidity(
            code && !supportedAirportCodes.has(code)
                ? 'Choose an airport from the supported-airports list.'
                : '',
        );
    }

    airportInputs.forEach((input) => {
        input.addEventListener('input', () => validateAirportInput(input));
        input.addEventListener('change', () => validateAirportInput(input));
    });

    // Initialize Map
    function initMap() {
        // Default view: Center of US
        map = L.map('map-container').setView([39.8283, -98.5795], 4);
        
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap'
        }).addTo(map);
    }

    initMap();

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        banner.style.display = 'none';

        airportInputs.forEach(validateAirportInput);
        if (!form.reportValidity()) {
            return;
        }

        const payload = {
            flight_date: document.getElementById('flight-date').value,
            dep_time: document.getElementById('dep-time').value,
            arr_time: document.getElementById('arr-time').value,
            airline: document.getElementById('airline').value,
            origin: document.getElementById('origin-airport').value.trim().toUpperCase(),
            destination: document.getElementById('dest-airport').value.trim().toUpperCase(), 
        };

        try {
            const resp = await fetch('/api/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });

            if (!resp.ok) {
                throw new Error('Server error');
            }

            const result = await resp.json();

            // ---- Banner ----
            banner.style.display = 'block';
            banner.classList.remove('alert-success', 'alert-danger', 'alert-warning');
            banner.classList.add(result.delayed ? 'alert-danger' : 'alert-success');

            let text = result.message || '';
            if (typeof result.probability === 'number') {
                text += ` (Probability of Delay: ${(result.probability * 100).toFixed(1)}%)`;
            }
            banner.textContent = text;

            // ---- Features table ----
            if (featuresBody) {
                featuresBody.innerHTML = '';
                if (result.features) {
                    Object.entries(result.features).forEach(([name, value]) => {
                        const tr = document.createElement('tr');
                        const tdName = document.createElement('td');
                        const tdValue = document.createElement('td');

                        tdName.textContent = name;
                        tdValue.textContent = value;
                        tdValue.className = 'text-end';

                        tr.appendChild(tdName);
                        tr.appendChild(tdValue);
                        featuresBody.appendChild(tr);
                    });
                }
            }

            // ---- Map Update ----
            if (result.route && result.route.origin_coords && result.route.dest_coords) {
                if (routeLayer) {
                    map.removeLayer(routeLayer);
                }

                const origin = result.route.origin_coords; // [lat, lon]
                const dest = result.route.dest_coords;

                const latlngs = [
                    origin,
                    dest
                ];

                routeLayer = L.layerGroup().addTo(map);

                // Draw line
                L.polyline(latlngs, {color: 'blue', weight: 3, opacity: 0.7}).addTo(routeLayer);

                // Add markers
                L.marker(origin).addTo(routeLayer).bindPopup(`Origin: ${payload.origin}`);
                L.marker(dest).addTo(routeLayer).bindPopup(`Dest: ${payload.destination}`);

                // Fit bounds
                map.fitBounds(L.polyline(latlngs).getBounds(), {padding: [50, 50]});
            }

        } catch (err) {
            console.error(err);
            banner.style.display = 'block';
            banner.classList.remove('alert-success', 'alert-danger');
            banner.classList.add('alert-warning');
            banner.textContent = 'Unable to get prediction. Please try again. ' + err.message;
        }
    });
});
