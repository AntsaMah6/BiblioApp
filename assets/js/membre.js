document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.btn-modif').forEach(function(btn) {
        btn.addEventListener('click', function() {
            document.getElementById('modal-modif').style.display = 'block';
            document.getElementById('modif-id').value = btn.dataset.id;
            document.getElementById('modif-nom').value = btn.dataset.nom;
            document.getElementById('modif-prenom').value = btn.dataset.prenom;
            document.getElementById('modif-age').value = btn.dataset.age;
            document.getElementById('modif-email').value = btn.dataset.email;
            document.getElementById('form-modif').action = '/membre/update/opupdate';
        });
    });
    document.querySelectorAll('.btn-suppr').forEach(function(btn) {
        btn.addEventListener('click', function() {
            if(confirm('Voulez-vous vraiment supprimer ce membre ?')) {
                window.location.href = '/membre/delete/' + btn.dataset.id;
            }
        });
    });
});
function closeModal() {
    document.getElementById('modal-modif').style.display = 'none';
}