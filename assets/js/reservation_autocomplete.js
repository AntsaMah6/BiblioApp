let livresReservablesData = [];
let membresData = [];
let selectedMembre = null;
let selectedLivre = null;
let currentFocus = -1;

// Charger les données au démarrage
document.addEventListener('DOMContentLoaded', function() {
    loadLivresReservables();
    loadMembres();
    initReservationAutocomplete();
    setupKeyboardNavigation();
    checkFormValidity();
});

// Charger les livres réservables (empruntés)
async function loadLivresReservables() {
    try {
        const response = await fetch('/api/livres/empruntes');
        if (response.ok) {
            livresReservablesData = await response.json();
            console.log('Livres réservables chargés:', livresReservablesData);
        } else {
            console.error('Erreur API livres empruntés:', response.status);
        }
    } catch (error) {
        console.error('Erreur chargement livres empruntés:', error);
    }
}

// Charger les membres
async function loadMembres() {
    try {
        const response = await fetch('/api/membres');
        if (response.ok) {
            membresData = await response.json();
            console.log('Membres chargés:', membresData);
        } else {
            console.error('Erreur API membres:', response.status);
        }
    } catch (error) {
        console.error('Erreur chargement membres:', error);
    }
}

// Initialiser l'autocomplétion
function initReservationAutocomplete() {
    const searchLivre = document.getElementById('search_livre');
    const searchMembre = document.getElementById('search_membre');
    
    // Autocomplétion livres réservables
    searchLivre.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase().trim();
        if (searchTerm.length < 2) {
            closeAllAutocompleteLists();
            return;
        }
        
        const results = livresReservablesData.filter(livre => 
            livre.titre.toLowerCase().includes(searchTerm) || 
            livre.auteur.toLowerCase().includes(searchTerm)
        );
        
        showReservationAutocomplete(results, 'livre', this);
    });
    
    // Autocomplétion membres
    searchMembre.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase().trim();
        if (searchTerm.length < 2) {
            closeAllAutocompleteLists();
            return;
        }
        
        const results = membresData.filter(membre => 
            membre.nom.toLowerCase().includes(searchTerm) || 
            membre.prenom.toLowerCase().includes(searchTerm) ||
            membre.email.toLowerCase().includes(searchTerm)
        );
        
        showReservationAutocomplete(results, 'membre', this);
    });
    
    // Fermer l'autocomplétion en cliquant ailleurs
    document.addEventListener('click', function(e) {
        closeAllAutocompleteLists(e.target);
    });
}

// Afficher les suggestions d'autocomplétion
function showReservationAutocomplete(items, type, inputElement) {
    const listId = type + '-autocomplete-list';
    let list = document.getElementById(listId);
    
    // Fermer toute liste existante
    closeAllAutocompleteLists();
    
    if (items.length === 0 || !inputElement.value) {
        return false;
    }
    
    // Créer la liste
    list = document.createElement('div');
    list.setAttribute('id', listId);
    list.setAttribute('class', 'autocomplete-items');
    inputElement.parentNode.appendChild(list);
    
    // Limiter à 10 résultats
    const limitedItems = items.slice(0, 10);
    
    // Ajouter les éléments
    limitedItems.forEach(item => {
        const element = document.createElement('div');
        
        if (type === 'livre') {
            // Pour les livres, afficher le statut d'emprunt
            const empruntInfo = item.emprunt ? 
                `<span style="color: #666; font-size: 0.9em;">(Emprunté jusqu'au ${item.emprunt.date_retour_prevue})</span>` : 
                '<span style="color: #666; font-size: 0.9em;">(Emprunté)</span>';
            
            element.innerHTML = `
                <strong>${escapeHtml(item.titre)}</strong> - ${escapeHtml(item.auteur)}<br>
                ${empruntInfo}
            `;
        } else {
            // Pour les membres, afficher le nombre d'emprunts et réservations
            const empruntsRestants = 3 - item.emprunts_actifs;
            const empruntsText = item.emprunts_actifs > 0 ? 
                `<span style="color: ${item.emprunts_actifs >= 3 ? '#dc3545' : '#28a745'}">(${item.emprunts_actifs}/3 emprunts - ${empruntsRestants} restants)</span>` :
                '<span style="color: #28a745">(0/3 emprunts - 3 restants)</span>';
            
            element.innerHTML = `
                <strong>${escapeHtml(item.nom)} ${escapeHtml(item.prenom)}</strong> 
                ${empruntsText}<br>
                <small>${escapeHtml(item.email)}</small>
            `;
            
            // Désactiver si le membre a déjà 3 emprunts
            if (item.emprunts_actifs >= 3) {
                element.style.opacity = '0.6';
                element.style.cursor = 'not-allowed';
                element.title = 'Membre a déjà 3 emprunts en cours';
            }
        }
        
        // Permettre la sélection
        element.addEventListener('click', function() {
            selectReservationItem(item, type, inputElement);
        });
        
        list.appendChild(element);
    });
}

// Sélectionner un élément
function selectReservationItem(item, type, inputElement) {
    if (type === 'membre') {
        // Vérifier si le membre peut emprunter
        if (item.emprunts_actifs >= 3) {
            alert('Ce membre a déjà 3 emprunts en cours et ne peut pas réserver de nouveaux livres.');
            return;
        }
        
        selectedMembre = item;
        document.getElementById('id_membre').value = item.id_membres;
        document.getElementById('membre-nom').textContent = item.nom;
        document.getElementById('membre-prenom').textContent = item.prenom;
        document.getElementById('membre-email').textContent = item.email;
        
        document.getElementById('selected-membre').classList.remove('hidden');
        inputElement.value = '';
        
    } else if (type === 'livre') {
        // Vérifier si le livre est déjà sélectionné
        if (selectedLivre && selectedLivre.id_livres === item.id_livres) {
            alert('Ce livre est déjà sélectionné.');
            return;
        }
        
        selectedLivre = item;
        document.getElementById('id_livre').value = item.id_livres;
        document.getElementById('livre-titre').textContent = item.titre;
        document.getElementById('livre-auteur').textContent = item.auteur;
        
        // Afficher la date de retour prévue
        const dateRetour = item.emprunt ? item.emprunt.date_retour_prevue : 'Date inconnue';
        document.getElementById('livre-statut').innerHTML = 
            ` <span style="color: #666; font-size: 0.9em;">(Retour prévu: ${dateRetour})</span>`;
        
        document.getElementById('selected-livre').classList.remove('hidden');
        inputElement.value = '';
    }
    
    closeAllAutocompleteLists();
    checkFormValidity();
}

// Effacer la sélection
function clearSelection(type) {
    if (type === 'membre') {
        selectedMembre = null;
        document.getElementById('id_membre').value = '';
        document.getElementById('selected-membre').classList.add('hidden');
        document.getElementById('search_membre').value = '';
    } else if (type === 'livre') {
        selectedLivre = null;
        document.getElementById('id_livre').value = '';
        document.getElementById('selected-livre').classList.add('hidden');
        document.getElementById('search_livre').value = '';
    }
    checkFormValidity();
}

// Vérifier si le formulaire est valide
function checkFormValidity() {
    const submitBtn = document.getElementById('submit-btn');
    if (selectedMembre && selectedLivre) {
        submitBtn.disabled = false;
    } else {
        submitBtn.disabled = true;
    }
}

// Fonctions utilitaires (reprises de autocomplete.js)
function closeAllAutocompleteLists(elmnt) {
    const items = document.getElementsByClassName('autocomplete-items');
    for (let i = 0; i < items.length; i++) {
        if (elmnt !== items[i] && elmnt !== document.getElementById('search_livre') && elmnt !== document.getElementById('search_membre')) {
            items[i].parentNode.removeChild(items[i]);
        }
    }
    currentFocus = -1;
}

function setupKeyboardNavigation() {
    document.addEventListener('keydown', function(e) {
        let items = document.getElementsByClassName('autocomplete-items');
        if (items.length === 0) return;
        
        items = items[0].getElementsByTagName('div');
        
        if (e.key === 'ArrowDown') {
            e.preventDefault();
            currentFocus++;
            addActive(items);
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            currentFocus--;
            addActive(items);
        } else if (e.key === 'Enter') {
            e.preventDefault();
            if (currentFocus > -1 && items[currentFocus]) {
                items[currentFocus].click();
            }
        } else if (e.key === 'Escape') {
            closeAllAutocompleteLists();
        }
    });
}

function addActive(items) {
    if (!items) return false;
    removeActive(items);
    
    if (currentFocus >= items.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = items.length - 1;
    
    items[currentFocus].classList.add('autocomplete-active');
}

function removeActive(items) {
    for (let i = 0; i < items.length; i++) {
        items[i].classList.remove('autocomplete-active');
    }
}

function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}