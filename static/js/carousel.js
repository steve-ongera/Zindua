let currentIndex = 0;

function showNext() {
    const items = document.querySelectorAll('.carousel-item');
    currentIndex = (currentIndex + 1) % items.length;
    const offset = -(currentIndex * 320); // Width of the item + margin
    document.querySelector('.carousel').style.transform = `translateX(${offset}px)`;
}

function showPrev() {
    const items = document.querySelectorAll('.carousel-item');
    currentIndex = (currentIndex - 1 + items.length) % items.length;
    const offset = -(currentIndex * 320); // Width of the item + margin
    document.querySelector('.carousel').style.transform = `translateX(${offset}px)`;
}

document.querySelector('.carousel-container::before').addEventListener('click', showPrev);
document.querySelector('.carousel-container::after').addEventListener('click', showNext);

// Set interval to automatically slide
setInterval(showNext, 3000); // Change every 3 seconds
