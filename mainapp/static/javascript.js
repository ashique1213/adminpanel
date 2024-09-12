document.addEventListener('DOMContentLoaded', function() {
    if (window.location.hash) {
        document.querySelector(window.location.hash).scrollIntoView({
            behavior: 'smooth'
        });
    }
});

// Show the 'home' section by default on page load
window.onload = function() {
    showSection('home');
};

function logout() {
    // Handle logout functionality here
    alert('Logged out');
}

