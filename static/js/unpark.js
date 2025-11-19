document.addEventListener("DOMContentLoaded", () => {
  const alertBox = document.getElementById("alertMess");
  const formScreen = document.getElementById("Form");
  const successScreen = document.getElementById("successScreen");
  const unparkForm = document.getElementById("UnparkForm");
  const successInfoBox = document.getElementById("successInfoBox");

  function showScreen(screen) {
    [formScreen, successScreen].forEach(s => s.classList.remove("active"));
    screen.classList.add("active");
  }

  function showAlert(text) {
    alertBox.textContent = text;
    alertBox.classList.add("show");
    setTimeout(() => alertBox.classList.remove("show"), 2000);
  }

  unparkForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const plate = document.getElementById("platenumber").value.trim().toUpperCase();

    if (!plate) {
      showAlert("Please enter a plate number.");
      return;
    }

    try {
      const response = await fetch("/unpark", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ platenumber: plate })
      });

      const result = await response.json();

      if (response.ok && result.success) {
        // Populate success screen
        const data = result.data;
        successInfoBox.textContent = `Driver's Name: ${data.driver_name}\nPlate Number: ${data.plate_number}\nParking Spot: ${data.spot}\nTime In: ${data.time_in}\nTime Out: ${data.time_out}`;
        showScreen(successScreen);
      } else {
        showAlert(result.error || "An error occurred.");
      }
    } catch (error) {
      showAlert("Network error. Please try again.");
    }
  });
});