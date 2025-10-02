// Fonctionnalité de recherche pour les livres
class LivreSearch {
    constructor() {
        this.searchInput = document.getElementById('search-input');
        this.livresContainer = document.getElementById('livres-container');
        this.noResults = document.getElementById('no-results');
        this.originalItems = this.livresContainer.innerHTML;
        this.init();
    }

    init() {
        this.searchInput.addEventListener('input', this.handleSearch.bind(this));
        this.searchInput.addEventListener('keyup', this.handleSearch.bind(this));
        
        // Ajouter un indicateur de recherche
        this.addLoadingIndicator();
    }

    addLoadingIndicator() {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'search-loading';
        loadingDiv.textContent = 'Recherche';
        this.searchInput.parentNode.appendChild(loadingDiv);
        this.loadingIndicator = loadingDiv;
    }

    handleSearch(event) {
        const searchTerm = this.searchInput.value.toLowerCase().trim();
        
        if (searchTerm === '') {
            this.showAllResults();
            return;
        }

        this.showLoading();
        this.performSearch(searchTerm);
    }

    showAllResults() {
        this.livresContainer.innerHTML = this.originalItems;
        this.noResults.style.display = 'none';
        this.livresContainer.style.display = 'block';
        this.hideLoading();
        this.reattachEventListeners();
    }

    performSearch(searchTerm) {
        // Simuler un délai pour l'animation (peut être supprimé)
        setTimeout(() => {
            const livres = document.querySelectorAll('.carousel-item');
            let hasResults = false;
            
            livres.forEach(livre => {
                const titre = livre.querySelector('h3').textContent.toLowerCase();
                const auteurElement = livre.querySelector('p');
                const auteur = auteurElement ? auteurElement.textContent.toLowerCase() : '';
                
                if (titre.includes(searchTerm) || auteur.includes(searchTerm)) {
                    livre.style.display = 'block';
                    livre.classList.add('search-match');
                    hasResults = true;
                } else {
                    livre.style.display = 'none';
                    livre.classList.remove('search-match');
                }
            });
            
            this.displayResults(hasResults);
        }, 150);
    }

    displayResults(hasResults) {
        if (hasResults) {
            this.noResults.style.display = 'none';
            this.livresContainer.style.display = 'block';
        } else {
            this.noResults.style.display = 'block';
            this.livresContainer.style.display = 'none';
        }
        
        this.hideLoading();
        this.reattachEventListeners();
    }

    showLoading() {
        if (this.loadingIndicator) {
            this.loadingIndicator.style.display = 'block';
        }
        document.getElementById('livres-carousel').classList.add('searching');
    }

    hideLoading() {
        if (this.loadingIndicator) {
            this.loadingIndicator.style.display = 'none';
        }
        document.getElementById('livres-carousel').classList.remove('searching');
    }

    reattachEventListeners() {
        // Réattacher les écouteurs d'événements pour les boutons de suppression
        document.querySelectorAll('.btn-suppr').forEach((btn) => {
            btn.addEventListener('click', function() {
                if(confirm('Voulez-vous vraiment supprimer ce livre ?')) {
                    window.location.href = '/livre/delete/' + this.dataset.id;
                }
            });
        });

        // Réattacher les écouteurs pour les boutons de modification
        document.querySelectorAll('.btn-primary').forEach((btn) => {
            if (btn.textContent.includes('Modifier')) {
                btn.addEventListener('click', function(e) {
                    // Le lien fonctionnera normalement
                });
            }
        });
    }
}

// Initialisation lorsque le DOM est chargé
document.addEventListener('DOMContentLoaded', function() {
    new LivreSearch();
});

// Fonction utilitaire pour effacer la recherche
function clearSearch() {
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.value = '';
        searchInput.dispatchEvent(new Event('input'));
    }
}

// Raccourci clavier pour la recherche (Ctrl+F)
document.addEventListener('keydown', function(e) {
    if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
        e.preventDefault();
        const searchInput = document.getElementById('search-input');
        if (searchInput) {
            searchInput.focus();
        }
    }
});

