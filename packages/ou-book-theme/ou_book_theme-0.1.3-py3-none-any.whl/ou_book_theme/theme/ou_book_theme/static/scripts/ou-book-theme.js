function ready() {
    const toggles = document.querySelectorAll('.ou-toggle');
    for(let toggle of toggles) {
        toggle.addEventListener('click', () => {
            toggle.classList.toggle('ou-toggle-hidden');
        });
    }
}

document.addEventListener("DOMContentLoaded", ready, false);
