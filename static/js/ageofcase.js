document.addEventListener("DOMContentLoaded", function() {
    function calculateTicketAges() {
        var tickets = document.querySelectorAll('[id^="age_"]');
        tickets.forEach(function(ticketElement) {
            var ticketNumber = ticketElement.id.split("_")[1]; // Extract ticket number from element ID
            var createdDateStr = ticketElement.getAttribute("data-created");
            var createdDate = new Date(createdDateStr);
            var currentDate = new Date();
            var formattedCurrentDate = currentDate.toISOString().slice(0, 19).replace('T', ' ');
            var currentDate = new Date(formattedCurrentDate);
            var ageInDays = Math.floor((currentDate - createdDate) / (1000 * 60 * 60 * 24));
            ticketElement.textContent = ageInDays + " days";
        });
    }

    calculateTicketAges();
});
