document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.querySelector('.sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    
    toggleButton.addEventListener('click', function() {
        sidebar.classList.toggle('active');
    });
});