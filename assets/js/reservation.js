document.addEventListener('DOMContentLoaded', function() {
    // Gestion des boutons honorer
    document.querySelectorAll('.btn-honorer').forEach(function(btn) {
        btn.addEventListener('click', function() {
            const reservationId = this.dataset.id;
            if(confirm('Honorer cette réservation ? Le livre sera automatiquement emprunté par ce membre.')) {
                window.location.href = '/reservation/honorer/' + reservationId;
            }
        });
    });
    
    // Gestion des boutons annuler
    document.querySelectorAll('.btn-annuler').forEach(function(btn) {
        btn.addEventListener('click', function() {
            const reservationId = this.dataset.id;
            if(confirm('Annuler cette réservation ?')) {
                window.location.href = '/reservation/annuler/' + reservationId;
            }
        });
    });
});