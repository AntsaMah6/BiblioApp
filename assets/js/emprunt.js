document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript emprunt chargé');
    
    // Gestion des confirmations de retour
    function handleReturnClick(e) {
        const target = e.target;
        const returnLink = target.closest('.btn-retour');
        
        if (returnLink) {
            e.preventDefault();
            e.stopPropagation();
            
            const empruntId = returnLink.href.split('/').pop();
            console.log('Clic sur retour pour emprunt ID:', empruntId);
            
            if (confirm('Confirmer le retour de ce livre ?')) {
                console.log('Redirection vers:', returnLink.href);
                window.location.href = returnLink.href;
            }
        }
    }
    
    // Ajouter l'écouteur d'événements
    document.addEventListener('click', handleReturnClick);
    
    // Debug: vérifier si les boutons sont trouvés
    const boutons = document.querySelectorAll('.btn-retour');
    console.log('Nombre de boutons .btn-retour trouvés:', boutons.length);
    
    boutons.forEach((btn, index) => {
        console.log(`Bouton ${index + 1}:`, btn.href);
    });
    
    // Auto-refresh des retards toutes les 5 minutes
    if (window.location.pathname === '/emprunt/retards') {
        console.log('Page retards - Auto-refresh activé');
        setInterval(() => {
            window.location.reload();
        }, 300000);
    }
    
});