document.addEventListener('DOMContentLoaded', () => {
    fetch('static/html/head.html')
        .then(response => response.text())
        .then(data => {
            const headElement = document.createElement('div');
            headElement.innerHTML = data;
            document.head.insertAdjacentHTML('beforeend', headElement.innerHTML);
        })
        .catch(error => console.error('Error loading head content:', error));
});