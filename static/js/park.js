document.addEventListener("DOMContentLoaded", () => {
  const alertBox = document.getElementById("alertMessage");

  const formScreen = document.getElementById("formScreen");
  const parkingScreen = document.getElementById("parkingScreen");
  const verifyScreen = document.getElementById("verifyScreen");
  const successScreen = document.getElementById("successScreen");

  const driverNameInput = document.getElementById("driverName");
  const plateNumberInput = document.getElementById("plateNumber");
  const chooseSpotBtn = document.getElementById("chooseSpotBtn");
  const selectedSpotSpan = document.getElementById("selectedSpot");
  const btnParkVehicle = document.getElementById("btnParkVehicle");
  const btnConfirmPark = document.getElementById("btnConfirmPark");

  // Add back button variables
  const btnBack = document.getElementById("btnBack");
  const btnBackParking = document.getElementById("btnBackParking");
  const btnBackVerify = document.getElementById("btnBackVerify");
  const btnBackSuccess = document.getElementById("btnBackSuccess");

  const leftSlots = document.getElementById("leftSlots");
  const rightSlots = document.getElementById("rightSlots");

  const verifyInfoBox = document.getElementById("verifyInfoBox");
  const successInfoBox = document.getElementById("successInfoBox");

  let tempOccupiedSlots = [];
  let selectedSpot = null;

  function showScreen(screen) {
    [formScreen, parkingScreen, verifyScreen, successScreen].forEach(
      (s) => s.classList.remove("active")
    );
    screen.classList.add("active");
  }

  function showAlert(text) {
    alertBox.textContent = text;
    alertBox.classList.add("show");
    setTimeout(() => alertBox.classList.remove("show"), 2000);
  }

  function createSlot(number) {
    const slot = document.createElement("div");
    slot.classList.add("slot");
    slot.textContent = "PARKING SPOT " + number;
    slot.tabIndex = 0;
    slot.setAttribute("role", "button");
    slot.setAttribute("aria-pressed", "false");

    if (tempOccupiedSlots.includes(number)) {
      slot.classList.add("occupied");
      slot.setAttribute("aria-disabled", "true");
    }
    if (selectedSpot === number) {
      slot.classList.add("selected");
      slot.setAttribute("aria-pressed", "true");
    }

    slot.addEventListener("click", () => {
      if (slot.classList.contains("occupied")) {
        showAlert("Parking Spot Occupied");
        return;
      }
      selectedSpot = number;
      updateSlotsSelection();
      selectedSpotSpan.textContent = selectedSpot;
      showScreen(formScreen);
    });

    return slot;
  }

  function setupSlots() {
    leftSlots.innerHTML = "";
    rightSlots.innerHTML = "";
    for (let i = 1; i <= 5; i++) leftSlots.appendChild(createSlot(i));
    for (let i = 6; i <= 10; i++) rightSlots.appendChild(createSlot(i));
  }

  function updateSlotsSelection() {
    [...leftSlots.children, ...rightSlots.children].forEach((slot) => {
      if (slot.textContent.endsWith(selectedSpot)) {
        slot.classList.add("selected");
        slot.setAttribute("aria-pressed", "true");
      } else {
        slot.classList.remove("selected");
        slot.setAttribute("aria-pressed", "false");
      }
    });
  }

  chooseSpotBtn.addEventListener("click", () => {
    setupSlots();
    showScreen(parkingScreen);
  });

  btnParkVehicle.addEventListener("click", (e) => {
    e.preventDefault();
    const name = driverNameInput.value.trim();
    const plate = plateNumberInput.value.trim();

    if (!name || !plate) {
      showAlert("Please fill in all the fields.");
      return;
    }
    if (!selectedSpot) {
      showAlert("Please choose a parking spot.");
      return;
    }

    verifyInfoBox.textContent = `Driver's Name: ${name}\nPlate Number: ${plate}\nParking Spot: ${selectedSpot}`;
    showScreen(verifyScreen);
  });

  // --- Send data to Flask when confirming ---
  btnConfirmPark.addEventListener("click", async () => {
    const name = driverNameInput.value.trim();
    const plate = plateNumberInput.value.trim();
    const spot = selectedSpot;

    if (!name || !plate || !spot) {
      showAlert("Missing information.");
      return;
    }

    try {
      const response = await fetch("/park", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({
          driver_name: name,
          plate_number: plate,
          spot_id: spot
        })
      });

      if (response.ok) {
        // Show success screen
        const now = new Date();
        const dateTimeString = now.toLocaleString();
        successInfoBox.textContent = `Driver's Name: ${name}\nPlate Number: ${plate}\nParking Spot: ${spot}\nDate & Time: ${dateTimeString}`;

        // Reset form
        driverNameInput.value = "";
        plateNumberInput.value = "";
        selectedSpot = null;
        selectedSpotSpan.textContent = "None";

        tempOccupiedSlots.push(spot);
        showScreen(successScreen);
      } else {
        showAlert("Failed to park vehicle. Try again.");
      }
    } catch (err) {
      showAlert("Error connecting to server.");
      console.error(err);
    }
  });

  // Add back button event listeners
  btnBack.addEventListener("click", () => window.location.href = "/dashboard");
  btnBackParking.addEventListener("click", () => showScreen(formScreen));
  btnBackVerify.addEventListener("click", () => showScreen(formScreen));
  btnBackSuccess.addEventListener("click", () => window.location.href = "/dashboard");

  showScreen(formScreen);
});