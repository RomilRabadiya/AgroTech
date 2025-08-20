document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript Loaded");

    // Fix Logout Button Issue
    let logoutBtn = document.querySelector("#logout-btn"); // Use querySelector
    if (logoutBtn) {
        logoutBtn.addEventListener("click", function (event) {
            event.preventDefault(); // Stop default action
            let confirmation = confirm("Are you sure you want to log out?");
            if (confirmation) {
                window.location.href = logoutBtn.href; // Redirect on confirmation
            }
        });
    } else {
        console.error("Logout button not found! Check your HTML.");
    }

   
});
