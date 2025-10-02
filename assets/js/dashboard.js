document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/stats')
        .then(response => response.json())
        .then(stats => {
            // Mettre à jour les compteurs
            document.querySelector('.stat-card:nth-child(1) .stat-number').textContent = stats.total_livres;
            document.querySelector('.stat-card:nth-child(2) .stat-number').textContent = stats.total_membres;
            document.querySelector('.stat-card:nth-child(3) .stat-number').textContent = stats.emprunts_actifs;
            
            const retardElement = document.querySelector('.stat-card:nth-child(4) .stat-number');
            retardElement.textContent = stats.emprunts_retard;
            
            // Changer la couleur si retards
            if (stats.emprunts_retard > 0) {
                retardElement.style.color = 'red';
                retardElement.style.fontWeight = 'bold';
            }

            const livresData = stats.livres_par_auteur;
            const membresData = stats.membres_par_age;
            
            // Graphique livres par auteur
            new Chart(document.getElementById('livresChart'), {
                type: 'bar',
                data: {
                    labels: Object.keys(livresData),
                    datasets: [{
                        label: 'Nombre de livres',
                        data: Object.values(livresData),
                        backgroundColor: '#1976d2'
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });

            // Graphique membres par âge
            new Chart(document.getElementById('membresChart'), {
                type: 'pie',
                data: {
                    labels: Object.keys(membresData).map(age => age + ' ans'),
                    datasets: [{
                        data: Object.values(membresData),
                        backgroundColor: ['#1976d2', '#2196f3', '#03a9f4', '#00bcd4', '#009688']
                    }]
                },
                options: {
                    responsive: true
                }
            });
        })
        .catch(error => console.error('Erreur lors du chargement des données:', error));
});