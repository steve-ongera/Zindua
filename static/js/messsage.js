// Wait for the page to load
document.addEventListener("DOMContentLoaded", function() {
    // Select all message divs
    const messages = document.querySelectorAll('.message');
    
    messages.forEach((msg, index) => {
        // Slide in animation from right
        setTimeout(() => {
            msg.classList.add('slide-in');
        }, index * 200); // Delay each message slightly

        // Auto remove after 5 seconds
        setTimeout(() => {
            msg.classList.add('fade-out');
            msg.addEventListener('transitionend', () => {
                msg.remove();
            });
        }, 5000);
    });
});