// QR Code generation function
function loadQRCode() {
    fetch('/.netlify/functions/api/qr', {
        method: 'GET',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('qr-code').src = `data:image/png;base64,${data.qr_image}`;
    })
    .catch(error => console.error('Error:', error));
}

// Rating submission function
function submitRating(rating) {
    fetch(`/.netlify/functions/api/submit_rating/${rating}`, {
        method: 'GET',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.redirect) {
            window.location.href = data.redirect;
        }
    })
    .catch(error => console.error('Error:', error));
}

// Star rating hover effects
function initializeStarRating() {
    document.querySelectorAll('.star').forEach(star => {
        star.addEventListener('mouseover', function() {
            this.style.color = '#ffd700';
            let prevSibling = this.previousElementSibling;
            while(prevSibling) {
                prevSibling.style.color = '#ffd700';
                prevSibling = prevSibling.previousElementSibling;
            }
        });
        
        star.addEventListener('mouseout', function() {
            document.querySelectorAll('.star').forEach(s => {
                s.style.color = '#ddd';
            });
        });
    });
}

// Initialize functions if elements exist
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('qr-code')) {
        loadQRCode();
    }
    if (document.querySelector('.stars')) {
        initializeStarRating();
    }
});

