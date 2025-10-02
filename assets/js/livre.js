document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.btn-modif').forEach(function(btn) {
        btn.addEventListener('click', function() {
            document.getElementById('modal-modif').style.display = 'block';
            document.getElementById('modif-id').value = btn.dataset.id;
            document.getElementById('modif-titre').value = btn.dataset.titre;
            document.getElementById('modif-auteur').value = btn.dataset.auteur;
            document.getElementById('form-modif').action = '/livre/update/opupdate';
        });
    });
    document.querySelectorAll('.btn-suppr').forEach(function(btn) {
        btn.addEventListener('click', function() {
            if(confirm('Voulez-vous vraiment supprimer ce livre ?')) {
                window.location.href = '/livre/delete/' + btn.dataset.id;
            }
        });
    });
});
function closeModal() {
    document.getElementById('modal-modif').style.display = 'none';
}