// Simulate automatic availability based on user actions (park/unpark)
// Uses localStorage to persist spot statuses across page loads

function loadSpotStatuses() {
  const spots = document.querySelectorAll('.spot-row');
  spots.forEach(spot => {
    const spotId = spot.getAttribute('data-spot');
    const status = localStorage.getItem(`spot-${spotId}`) || 'available';
    updateSpotStatus(spotId, status);
  });
}

function updateSpotStatus(spotId, status) {
  const spotRow = document.querySelector(`.spot-row[data-spot="${spotId}"]`);
  const statusDiv = spotRow.querySelector('.spot-status');
  statusDiv.className = `spot-status ${status}`;
  statusDiv.textContent = status.toUpperCase();
  localStorage.setItem(`spot-${spotId}`, status);
}

// Simulate parking a spot (e.g., from park page)
function parkSpot(spotId) {
  updateSpotStatus(spotId, 'unavailable');
}

// Simulate unparking a spot (e.g., from unpark page)
function unparkSpot(spotId) {
  updateSpotStatus(spotId, 'available');
}

// Load statuses on page load
document.addEventListener('DOMContentLoaded', loadSpotStatuses);

// Expose functions for testing (e.g., in browser console)
window.parkSpot = parkSpot;
window.unparkSpot = unparkSpot;