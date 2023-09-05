document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const productItems = document.querySelectorAll('.pro');

    searchInput.addEventListener('input', function() {
        const searchTerm = searchInput.value.toLowerCase();

        productItems.forEach(function(item) {
            const productText = item.textContent.toLowerCase();
            if (productText.includes(searchTerm)) {
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        });
    });
});
