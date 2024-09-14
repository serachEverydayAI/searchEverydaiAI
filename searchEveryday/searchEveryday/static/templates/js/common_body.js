document.addEventListener('DOMContentLoaded', () => {
    fetch('static/html/body.html')
        .then(response => response.text())
        .then(data => {
            const bodyElement = document.createElement('div');
            bodyElement.innerHTML = data;
            document.body.insertAdjacentHTML('beforeend', bodyElement.innerHTML);
        })
        .catch(error => console.error('Error loading body content:', error));
});
