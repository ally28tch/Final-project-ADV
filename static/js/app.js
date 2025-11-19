document.addEventListener('DOMContentLoaded', () => {
  const chooseSpotBtn = document.getElementById('chooseSpotBtn');
  const selectedSpotSpan = document.getElementById('selectedSpot');
  const backBtn = document.getElementById('backBtn');
  const parkForm = document.getElementById('parkForm');

  const parkingSpots = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'];
  let selectedSpot = null;

  chooseSpotBtn.addEventListener('click', () => {
    let spot = prompt(`Choose your parking spot (1-10):\nAvailable spots: ${parkingSpots.join(', ')}`, selectedSpot || '');
    if (spot && parkingSpots.includes(spot.trim())) {
      selectedSpot = spot.trim();
      selectedSpotSpan.textContent = selectedSpot;
    } else if (spot !== null) {
      alert("Invalid choice. Please enter a spot number between 1 and 10.");
    }
  });

  parkForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const driverName = parkForm.driverName.value.trim();
    const plateNumber = parkForm.plateNumber.value.trim();

    if (!driverName || !plateNumber) {
      alert("Please fill in all the fields.");
      return;
    }

    if (!selectedSpot) {
      alert("Please choose a parking spot.");
      return;
    }

    alert(`Vehicle parked!\nDriver: ${driverName}\nPlate Number: ${plateNumber}\nSpot: ${selectedSpot}`);

    parkForm.reset();
    selectedSpot = null;
    selectedSpotSpan.textContent = "None";
  });

  backBtn.addEventListener('click', () => {
    window.location.href = '/dashboard';
  });
});