document.addEventListener('DOMContentLoaded', function() {
    const imgContainers = document.querySelectorAll('.img-container');

    imgContainers.forEach(container => {
        const img = container.querySelector('img');

        // Événement de clic pour le zoom de l'image
        img.addEventListener('click', function() {
            container.classList.toggle('zoomed');
            img.style.maxWidth = container.classList.contains('zoomed') ? 'none' : '100%';
            img.style.width = 'auto';
            img.style.height = 'auto';
        });

        // Ajoute un effet de zoom progressif au survol
        container.addEventListener('mouseenter', function() {
            container.style.transform = 'scale(1.03)';
            container.style.transition = 'transform 0.3s ease';
        });

        container.addEventListener('mouseleave', function() {
            container.style.transform = 'scale(1)';
        });
    });

    // Fonctionnalité de recherche
    const searchInput = document.getElementById('searchInput');

    searchInput.addEventListener('input', function() {
        const query = this.value.toLowerCase();
        const familySections = document.querySelectorAll('.family-section');

        familySections.forEach(section => {
            const title = section.getAttribute('data-title').toLowerCase();
            if (title.includes(query)) {
                section.style.display = ''; // Afficher la section
            } else {
                section.style.display = 'none'; // Masquer la section
            }
        });
    });
});
