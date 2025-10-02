class Carousel {
    constructor(containerId, itemsPerPage = 10) {
        this.container = document.getElementById(containerId);
        this.itemsPerPage = itemsPerPage;
        this.currentPage = 1;
        this.totalPages = 1;
        this.items = [];
        
        this.init();
    }
    
    init() {
        // Récupérer tous les éléments du carrousel
        this.items = Array.from(this.container.querySelectorAll('.carousel-item'));
        this.totalPages = Math.ceil(this.items.length / this.itemsPerPage);
        
        // Créer la navigation si nécessaire
        if (this.totalPages > 1) {
            this.createNavigation();
        }
        
        this.showPage(1);
    }
    
    createNavigation() {
        const nav = document.createElement('div');
        nav.className = 'carousel-nav';
        
        nav.innerHTML = `
            <div class="carousel-info">Page <span id="current-page">1</span> sur ${this.totalPages}</div>
            <div class="carousel-buttons">
                <button class="btn btn-primary" id="prev-btn">Précédent</button>
                <button class="btn btn-primary" id="next-btn">Suivant</button>
            </div>
        `;
        
        this.container.appendChild(nav);
        
        // Événements
        document.getElementById('prev-btn').addEventListener('click', () => this.prevPage());
        document.getElementById('next-btn').addEventListener('click', () => this.nextPage());
    }
    
    showPage(page) {
        this.currentPage = page;
        
        // Masquer tous les éléments
        this.items.forEach(item => item.classList.remove('active'));
        
        // Afficher les éléments de la page courante
        const startIndex = (page - 1) * this.itemsPerPage;
        const endIndex = startIndex + this.itemsPerPage;
        
        this.items.slice(startIndex, endIndex).forEach(item => {
            item.classList.add('active');
        });
        
        // Mettre à jour la navigation
        const pageInfo = this.container.querySelector('#current-page');
        if (pageInfo) {
            pageInfo.textContent = page;
        }
        
        // Gérer l'état des boutons
        this.updateButtonStates();
    }
    
    prevPage() {
        if (this.currentPage > 1) {
            this.showPage(this.currentPage - 1);
        }
    }
    
    nextPage() {
        if (this.currentPage < this.totalPages) {
            this.showPage(this.currentPage + 1);
        }
    }
    
    updateButtonStates() {
        const prevBtn = this.container.querySelector('#prev-btn');
        const nextBtn = this.container.querySelector('#next-btn');
        
        if (prevBtn) {
            prevBtn.disabled = this.currentPage === 1;
        }
        if (nextBtn) {
            nextBtn.disabled = this.currentPage === this.totalPages;
        }
    }
}

// Initialiser les carrousels sur la page
document.addEventListener('DOMContentLoaded', function() {
    const carousels = document.querySelectorAll('.carousel');
    window.carousels = []; // Stocker globalement les instances
    
    carousels.forEach((carousel, index) => {
        const instance = new Carousel(carousel.id, 10);
        window.carousels.push(instance);
    });
});