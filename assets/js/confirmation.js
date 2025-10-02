// confirmation.js - Version corrigée et simplifiée
class ConfirmationSystem {
    constructor() {
        this.currentActionUrl = '';
        this.init();
    }
    
    init() {
        // Créer le modal s'il n'existe pas
        this.createModal();
        
        this.modal = document.getElementById('confirmationModal');
        this.message = document.getElementById('confirmationMessage');
        this.confirmBtn = document.getElementById('confirmAction');
        this.cancelBtn = document.getElementById('cancelAction');
        
        if (!this.modal || !this.message || !this.confirmBtn || !this.cancelBtn) {
            console.error('Éléments du modal de confirmation non trouvés');
            return;
        }
        
        this.confirmBtn.addEventListener('click', () => this.executeAction());
        this.cancelBtn.addEventListener('click', () => this.hide());
        
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) this.hide();
        });
        
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.modal.style.display === 'block') {
                this.hide();
            }
        });
        
        // Gestion des liens de suppression
        this.attachDeleteListeners();
    }
    
    createModal() {
        if (document.getElementById('confirmationModal')) {
            return; // Le modal existe déjà
        }
        
        const modalHTML = `
            <div id="confirmationModal" class="confirmation-modal">
                <div class="confirmation-content">
                    <h3>Confirmation de suppression</h3>
                    <p id="confirmationMessage">Êtes-vous sûr de vouloir effectuer cette action ?</p>
                    <div class="confirmation-buttons">
                        <button id="confirmAction" class="btn btn-confirm">Confirmer</button>
                        <button id="cancelAction" class="btn btn-cancel">Annuler</button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHTML);
    }
    
    attachDeleteListeners() {
        // Écouter tous les clics sur les liens de suppression
        document.addEventListener('click', (e) => {
            const target = e.target.closest('a[href*="/delete/"]');
            if (target) {
                e.preventDefault();
                this.handleDeleteClick(target);
            }
        });
    }
    
    handleDeleteClick(deleteLink) {
        // Récupérer le nom du membre depuis la carte
        const itemCard = deleteLink.closest('.item-card');
        let itemName = 'ce membre';
        
        if (itemCard) {
            const nameElement = itemCard.querySelector('h3');
            if (nameElement) {
                itemName = `"${nameElement.textContent.trim()}"`;
            }
        }
        
        this.show(
            `Êtes-vous sûr de vouloir supprimer ${itemName} ? Cette action est irréversible.`,
            deleteLink.href
        );
    }
    
    show(message, actionUrl) {
        this.message.textContent = message;
        this.currentActionUrl = actionUrl;
        this.modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
    }
    
    hide() {
        this.modal.style.display = 'none';
        document.body.style.overflow = '';
        this.currentActionUrl = '';
    }
    
    executeAction() {
        if (this.currentActionUrl) {
            console.log('Exécution de l\'action:', this.currentActionUrl);
            window.location.href = this.currentActionUrl;
        }
        this.hide();
    }
}

// Initialisation globale
document.addEventListener('DOMContentLoaded', function() {
    console.log('Initialisation du système de confirmation');
    window.confirmationSystem = new ConfirmationSystem();
});