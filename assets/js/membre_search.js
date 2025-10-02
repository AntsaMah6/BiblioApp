// Fonctionnalité de recherche pour les membres
class MembreSearch {
    constructor() {
        this.searchInput = document.getElementById('search-input');
        this.membresContainer = document.getElementById('search-results-container');
        this.noResults = document.getElementById('no-results');
        this.originalCarousel = document.getElementById('membres-carousel');
        
        console.log('Éléments trouvés:', {
            searchInput: this.searchInput,
            membresContainer: this.membresContainer,
            noResults: this.noResults,
            originalCarousel: this.originalCarousel
        });
        
        if (!this.searchInput || !this.membresContainer) {
            console.error('Éléments de recherche non trouvés dans le DOM');
            return;
        }
        
        this.originalContent = this.membresContainer.innerHTML;
        this.init();
    }

    init() {
        console.log('Initialisation de la recherche des membres');
        this.searchInput.addEventListener('input', this.debounce(this.handleSearch.bind(this), 300));
        this.addLoadingIndicator();
        this.addResultsCounter();
    }

    addLoadingIndicator() {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'search-loading';
        loadingDiv.textContent = 'Recherche en cours';
        loadingDiv.style.display = 'none';
        this.searchInput.parentNode.appendChild(loadingDiv);
        this.loadingIndicator = loadingDiv;
    }

    addResultsCounter() {
        const counterDiv = document.createElement('div');
        counterDiv.className = 'search-results-count';
        counterDiv.style.display = 'none';
        this.membresContainer.parentNode.insertBefore(counterDiv, this.membresContainer);
        this.resultsCounter = counterDiv;
    }

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    async handleSearch(event) {
        const searchTerm = this.searchInput.value.trim();
        console.log('Recherche:', searchTerm);
        
        if (searchTerm === '') {
            this.showAllResults();
            return;
        }

        this.showLoading();
        
        try {
            const membres = await this.searchOnServer(searchTerm);
            console.log('Résultats reçus:', membres);
            this.displaySearchResults(membres, searchTerm);
        } catch (error) {
            console.error('Erreur lors de la recherche:', error);
            this.displaySearchResults([], searchTerm);
        } finally {
            this.hideLoading();
        }
    }

    async searchOnServer(searchTerm) {
        const url = `/api/membres/search?q=${encodeURIComponent(searchTerm)}`;
        console.log('Requête API:', url);
        
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Erreur HTTP: ${response.status}`);
        }
        return await response.json();
    }

    displaySearchResults(membres, searchTerm) {
        console.log('Affichage des résultats:', membres.length);
        
        if (membres.length === 0) {
            this.noResults.style.display = 'block';
            this.originalCarousel.style.display = 'none';
            this.updateResultsCounter(0, searchTerm);
            return;
        }

        this.noResults.style.display = 'none';
        this.originalCarousel.style.display = 'none';
        
        let resultsHTML = '<div class="items-grid">';
        
        membres.forEach(membre => {
            resultsHTML += `
            <div class="item-card">
                <h3>${this.highlightText(membre.nom + ' ' + membre.prenom, searchTerm)}</h3>
                <p><strong>Âge:</strong> ${membre.age} ans</p>
                <p><strong>Email:</strong> ${this.highlightText(membre.email, searchTerm)}</p>
                <div class="item-actions">
                    <a href="/membre/update/${membre.id_membres}" class="btn btn-primary">Modifier</a>
                    <a href="/membre/delete/${membre.id_membres}" class="btn btn-danger">Supprimer</a>
                </div>
            </div>
            `;
        });
        
        resultsHTML += '</div>';
        
        this.membresContainer.innerHTML = `
            ${resultsHTML}
            <div id="no-results" class="no-results-message" style="display: none;">
                Aucun membre trouvé pour votre recherche.
            </div>
        `;
        
        this.updateResultsCounter(membres.length, searchTerm);
        // Plus besoin de reattacherEventListeners car confirmation.js gère tout
    }

    highlightText(text, searchTerm) {
        if (!searchTerm) return text;
        try {
            const regex = new RegExp(`(${this.escapeRegex(searchTerm)})`, 'gi');
            return text.replace(regex, '<mark>$1</mark>');
        } catch (e) {
            return text;
        }
    }

    escapeRegex(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    updateResultsCounter(count, searchTerm) {
        if (this.resultsCounter) {
            if (count === 0 && searchTerm) {
                this.resultsCounter.textContent = `Aucun résultat trouvé pour "${searchTerm}"`;
                this.resultsCounter.style.display = 'block';
            } else if (count > 0) {
                this.resultsCounter.textContent = `${count} membre(s) trouvé(s) pour "${searchTerm}"`;
                this.resultsCounter.style.display = 'block';
            } else {
                this.resultsCounter.style.display = 'none';
            }
        }
    }

    showAllResults() {
        this.membresContainer.innerHTML = this.originalContent;
        this.noResults.style.display = 'none';
        
        if (this.resultsCounter) {
            this.resultsCounter.style.display = 'none';
        }
        
        setTimeout(() => {
            if (window.carousels && window.carousels.length > 0) {
                window.carousels.forEach(carousel => {
                    carousel.showPage(1);
                });
            }
        }, 100);
    }

    showLoading() {
        if (this.loadingIndicator) {
            this.loadingIndicator.style.display = 'block';
        }
    }

    hideLoading() {
        if (this.loadingIndicator) {
            this.loadingIndicator.style.display = 'none';
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM chargé - initialisation recherche membres');
    new MembreSearch();
});