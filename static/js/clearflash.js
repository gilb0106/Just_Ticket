function hideFlashMessage() {
    setTimeout(function() {
        var flashMessages = document.getElementById('flash-messages');
        if (flashMessages) {
            flashMessages.style.display = 'none';
        }
    }, 5000);
}

document.addEventListener('DOMContentLoaded', function() {
    hideFlashMessage();
});
