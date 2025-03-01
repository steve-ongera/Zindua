document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('pickupModal');
    const changeBtn = document.getElementById('changePickupBtn');
    const closeBtn = document.querySelector('.close-modal');
    const stationBtns = document.querySelectorAll('.select-station-btn');
    const searchInput = document.getElementById('stationSearch');
    
    // Open modal
    changeBtn.addEventListener('click', function(e) {
        e.preventDefault();
        modal.style.display = 'block';
    });
    
    // Close modal
    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });
    
    // Close modal when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
    
    // Handle station selection
    stationBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const stationId = this.getAttribute('data-station-id');
            const stationName = this.getAttribute('data-station-name');
            const stationDetails = this.getAttribute('data-station-details');
            
            // Update the displayed pickup station
            document.querySelector('.station-details').innerHTML = 
                stationName + '<br>' + stationDetails;
            
            // Send AJAX request to update the pickup station
            updatePickupStation(stationId);
            
            // Close the modal
            modal.style.display = 'none';
        });
    });
    
    // Search functionality
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const stationItems = document.querySelectorAll('.station-item');
        
        stationItems.forEach(item => {
            const stationName = item.querySelector('h4').textContent.toLowerCase();
            const stationDetails = item.querySelector('p').textContent.toLowerCase();
            
            if (stationName.includes(searchTerm) || stationDetails.includes(searchTerm)) {
                item.style.display = 'flex';
            } else {
                item.style.display = 'none';
            }
        });
    });
    
    // Function to send AJAX request to update pickup station
    function updatePickupStation(stationId) {
        fetch('/update-pickup-station/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                'station_id': stationId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Pickup station updated successfully');
            } else {
                console.error('Error updating pickup station');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
    
    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});