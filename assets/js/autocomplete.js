let livresData = [];
let membresData = [];
let selectedMembre = null;
let selectedLivres = []; // Tableau pour stocker les livres sélectionnés
let currentFocus = -1;

// Charger les données au démarrage
document.addEventListener('DOMContentLoaded', function() {
    loadLivres();
    loadMembres();
    initAutocomplete();
    setupKeyboardNavigation();
    updateLivresCount();
});

// Charger les livres disponibles
async function loadLivres() {
    try {
        const response = await fetch('/api/livres/disponibles');
        if (response.ok) {
            livresData = await response.json();
        } else {
            console.error('Erreur API livres:', response.status);
        }
    } catch (error) {
        console.error('Erreur chargement livres:', error);
    }
}

// Charger les membres
async function loadMembres() {
    try {
        const response = await fetch('/api/membres');
        if (response.ok) {
            membresData = await response.json();
        } else {
            console.error('Erreur API membres:', response.status);
        }
    } catch (error) {
        console.error('Erreur chargement membres:', error);
    }
}

// Initialiser l'autocomplétion
function initAutocomplete() {
    const searchLivre = document.getElementById('search_livre');
    const searchMembre = document.getElementById('search_membre');
    
    // Autocomplétion livres
    searchLivre.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase().trim();
        if (searchTerm.length < 2) {
            closeAllAutocompleteLists();
            return;
        }
        
        // Filtrer les livres déjà sélectionnés
        const availableLivres = livresData.filter(livre => 
            !selectedLivres.some(selected => selected.id_livres === livre.id_livres)
        );
        
        const results = availableLivres.filter(livre => 
            livre.titre.toLowerCase().includes(searchTerm) || 
            livre.auteur.toLowerCase().includes(searchTerm)
        );
        
        showAutocomplete(results, 'livre', this);
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
        
        showAutocomplete(results, 'membre', this);
    });
    
    // Fermer l'autocomplétion en cliquant ailleurs
    document.addEventListener('click', function(e) {
        closeAllAutocompleteLists(e.target);
    });
}

// Afficher les suggestions d'autocomplétion
function showAutocomplete(items, type, inputElement) {
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
            element.innerHTML = `<strong>${escapeHtml(item.titre)}</strong> - ${escapeHtml(item.auteur)}`;
        } else {
            // Afficher le nombre d'emprunts actifs
            const empruntsRestants = 3 - item.emprunts_actifs;
            const empruntsText = item.emprunts_actifs > 0 
                ? `<span style="color: ${item.emprunts_actifs >= 3 ? '#dc3545' : '#28a745'}">(${item.emprunts_actifs}/3 emprunts - ${empruntsRestants} restants)</span>`
                : '<span style="color: #28a745">(0/3 emprunts - 3 restants)</span>';
            
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
        
        // Ne permettre la sélection que si le membre peut emprunter
        if (type !== 'membre' || item.emprunts_actifs < 3) {
            element.addEventListener('click', function() {
                selectItem(item, type, inputElement);
            });
        }
        
        list.appendChild(element);
    });
}

// Sélectionner un élément
function selectItem(item, type, inputElement) {
    if (type === 'membre') {
        if (item.emprunts_actifs >= 3) {
            alert('Ce membre a déjà 3 emprunts en cours et ne peut pas emprunter de nouveaux livres.');
            return;
        }
        
        selectedMembre = item;
        document.getElementById('id_membre').value = item.id_membres;
        document.getElementById('membre-nom').textContent = item.nom;
        document.getElementById('membre-prenom').textContent = item.prenom;
        document.getElementById('membre-email').textContent = item.email;
        
        // Afficher le nombre d'emprunts dans la sélection
        const empruntsRestants = 3 - item.emprunts_actifs;
        const empruntsInfo = document.createElement('span');
        empruntsInfo.innerHTML = ` <span style="color: ${empruntsRestants > 0 ? '#28a745' : '#dc3545'}">(${item.emprunts_actifs}/3 emprunts - ${empruntsRestants} restants)</span>`;
        document.getElementById('selected-membre').appendChild(empruntsInfo);
        
        document.getElementById('selected-membre').classList.remove('hidden');
        inputElement.value = '';
        
    } else if (type === 'livre') {
        // Vérifier si le livre est déjà sélectionné
        if (selectedLivres.some(livre => livre.id_livres === item.id_livres)) {
            alert('Ce livre est déjà sélectionné.');
            return;
        }
        
        // Vérifier la limite de livres
        if (selectedLivres.length >= 3) {
            alert('Maximum 3 livres par emprunt.');
            return;
        }
        
        // Vérifier si le membre peut emprunter ce nombre de livres supplémentaires
        if (selectedMembre) {
            const totalAfterSelection = selectedMembre.emprunts_actifs + selectedLivres.length + 1;
            if (totalAfterSelection > 3) {
                alert(`Ce membre ne peut emprunter que ${3 - selectedMembre.emprunts_actifs} livre(s) supplémentaire(s).`);
                return;
            }
        }
        
        // Ajouter le livre à la sélection
        selectedLivres.push(item);
        addLivreToSelection(item);
        inputElement.value = '';
    }
    
    closeAllAutocompleteLists();
    updateLivresCount();
    checkFormValidity();
}

// Ajouter un livre à la liste de sélection
function addLivreToSelection(livre) {
    const livresList = document.getElementById('livres-list');
    const livreElement = document.createElement('div');
    livreElement.className = 'livre-item';
    livreElement.innerHTML = `
        <div class="livre-info">
            <strong>${escapeHtml(livre.titre)}</strong> - ${escapeHtml(livre.auteur)}
        </div>
        <div class="livre-actions">
            <button type="button" onclick="removeLivre(${livre.id_livres})" class="remove-livre">×</button>
        </div>
    `;
    livresList.appendChild(livreElement);
    
    // CORRECTION : Ajouter un champ hidden pour chaque livre
    const container = document.getElementById('livres-ids-container');
    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'id_livres';  // Même nom pour tous les livres
    input.value = livre.id_livres;
    input.className = 'livre-id-input';  // Classe pour identification
    container.appendChild(input);
    
    console.log(`Livre ${livre.id_livres} ajouté à la sélection`);
}

// Supprimer un livre de la sélection
function removeLivre(livreId) {
    // Retirer du tableau
    selectedLivres = selectedLivres.filter(livre => livre.id_livres !== livreId);
    
    // Retirer de l'affichage
    const livresList = document.getElementById('livres-list');
    const elements = livresList.getElementsByClassName('livre-item');
    for (let element of elements) {
        if (element.querySelector('button').onclick.toString().includes(livreId)) {
            element.remove();
            break;
        }
    }
    
    // Retirer le champ hidden
    const container = document.getElementById('livres-ids-container');
    const inputs = container.querySelectorAll('input[name="id_livres"]');
    for (let input of inputs) {
        if (parseInt(input.value) === livreId) {
            input.remove();
            break;
        }
    }
    
    updateLivresCount();
    checkFormValidity();
}

// Mettre à jour le compteur de livres
function updateLivresCount() {
    const countElement = document.getElementById('livres-count');
    countElement.textContent = selectedLivres.length;
    
    const countContainer = document.querySelector('.livres-count');
    if (selectedLivres.length >= 3) {
        countContainer.classList.add('warning');
    } else {
        countContainer.classList.remove('warning');
    }
}

// Effacer la sélection
function clearSelection(type) {
    if (type === 'membre') {
        selectedMembre = null;
        document.getElementById('id_membre').value = '';
        document.getElementById('selected-membre').classList.add('hidden');
        document.getElementById('search_membre').value = '';
        
        // Vider aussi la sélection de livres si le membre change
        clearLivresSelection();
    }
    checkFormValidity();
}

// Vider la sélection de livres
function clearLivresSelection() {
    selectedLivres = [];
    document.getElementById('livres-list').innerHTML = '';
    document.getElementById('livres-ids-container').innerHTML = '';
    document.getElementById('search_livre').value = '';
    updateLivresCount();
}

// Vérifier si le formulaire est valide
function checkFormValidity() {
    const submitBtn = document.getElementById('submit-btn');
    if (selectedMembre && selectedLivres.length > 0) {
        submitBtn.disabled = false;
    } else {
        submitBtn.disabled = true;
    }
}

// Les autres fonctions restent les mêmes...
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