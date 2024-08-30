document.getElementById('allocationForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    const data = new URLSearchParams(formData).toString();

    fetch('/allocate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: data
    })
    .then(response => response.json())
    .then(result => {
        const resultDiv = document.getElementById('result');
        if (result.status === 'success') {
            resultDiv.innerHTML = `
                <h2 class="success">Allocation Successful</h2>
                <p><strong>Route Number:</strong> ${result.route_number}</p>
                <p><strong>Route Stops:</strong> ${result.route_stops}</p>
                <p><strong>Route Timings:</strong> ${result.route_timings}</p>
            `;
        } else {
            resultDiv.innerHTML = `
                <h2 class="error">Error</h2>
                <p>${result.message}</p>
            `;
        }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('showSchedule').addEventListener('click', function() {
    fetch('/show_schedule')
    .then(response => response.json())
    .then(data => {
        const scheduleDiv = document.getElementById('schedule');
        let html = '<h2>Allocated Schedule</h2>';
        if (Object.keys(data).length === 0) {
            html += '<p>No schedules allocated yet.</p>';
        } else {
            html += '<table><thead><tr><th>Route Number</th><th>Driver</th><th>Conductor</th><th>Stops</th><th>Timings</th></tr></thead><tbody>';
            for (const [routeNumber, details] of Object.entries(data)) {
                html += `<tr>
                    <td>${routeNumber}</td>
                    <td>${details.driver}</td>
                    <td>${details.conductor}</td>
                    <td>${details.route_stops}</td>
                    <td>${details.route_timings}</td>
                </tr>`;
            }
            html += '</tbody></table>';
        }
        scheduleDiv.innerHTML = html;
    })
    .catch(error => console.error('Error:', error));
});
