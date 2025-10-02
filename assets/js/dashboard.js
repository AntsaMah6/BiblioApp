document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/stats')
        .then(response => response.json())
        .then(stats => {
            updateStatsCards(stats);
            createCharts(stats);
            updateOccupationStats(stats); // AJOUTEZ CETTE LIGNE
            updateRecentActivity(stats.recent_activity);
        })
        .catch(error => console.error('Erreur lors du chargement des données:', error));
});

function updateStatsCards(stats) {
    // Mettre à jour les compteurs principaux
    document.querySelector('.stat-card:nth-child(1) .stat-number').textContent = stats.total_livres;
    document.querySelector('.stat-card:nth-child(2) .stat-number').textContent = stats.total_membres;
    document.querySelector('.stat-card:nth-child(3) .stat-number').textContent = stats.emprunts_actifs;
    document.querySelector('.stat-card:nth-child(4) .stat-number').textContent = stats.livres_disponibles;
    document.querySelector('.stat-card:nth-child(5) .stat-number').textContent = stats.reservations_attente;
    
    const retardElement = document.querySelector('.stat-card:nth-child(6) .stat-number');
    retardElement.textContent = stats.emprunts_retard;
    
    // Appliquer les styles de warning pour les retards
    if (stats.emprunts_retard > 0) {
        retardElement.parentElement.classList.add('warning');
    }

    // Ajouter des indicateurs de tendance
    addTrendIndicators(stats);
}

function addTrendIndicators(stats) {
    // Exemple d'indicateurs de tendance (à adapter avec vos données réelles)
    const trends = {
        emprunts_actifs: 'up',
        emprunts_retard: stats.emprunts_retard > 0 ? 'up' : 'down',
        livres_disponibles: 'stable'
    };

    Object.keys(trends).forEach((key, index) => {
        const card = document.querySelector(`.stat-card:nth-child(${index + 3})`);
        const trend = trends[key];
        
        if (trend !== 'stable') {
            const trendElement = document.createElement('div');
            trendElement.className = `stat-trend trend-${trend}`;
            trendElement.textContent = trend === 'up' ? '↑' : '↓';
            card.appendChild(trendElement);
        }
    });
}

function createCharts(stats) {
    // Palette de couleurs variées
    const colorPalette = [
        '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
        '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9',
        '#F8C471', '#82E0AA', '#F1948A', '#85C1E9', '#D7BDE2',
        '#F9E79F', '#A9DFBF', '#F5B7B1', '#AED6F1', '#D2B4DE'
    ];

    // Graphique livres par auteur (Top 10)
    const topAuteurs = Object.entries(stats.livres_par_auteur)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10);

    new Chart(document.getElementById('livresChart'), {
        type: 'bar',
        data: {
            labels: topAuteurs.map(([auteur]) => auteur),
            datasets: [{
                label: 'Nombre de livres',
                data: topAuteurs.map(([, count]) => count),
                backgroundColor: colorPalette.slice(0, topAuteurs.length),
                borderColor: colorPalette.slice(0, topAuteurs.length).map(color => color + 'CC'),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Top 10 des auteurs'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });

    // Graphique membres par âge
    new Chart(document.getElementById('membresChart'), {
        type: 'doughnut',
        data: {
            labels: Object.keys(stats.membres_par_age).map(age => age + ' ans'),
            datasets: [{
                data: Object.values(stats.membres_par_age),
                backgroundColor: colorPalette.slice(5, 5 + Object.keys(stats.membres_par_age).length),
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'right'
                }
            },
            cutout: '50%'
        }
    });

    // Nouveau graphique : Statut des emprunts
    if (stats.emprunts_par_statut) {
        new Chart(document.getElementById('empruntsChart'), {
            type: 'pie',
            data: {
                labels: Object.keys(stats.emprunts_par_statut),
                datasets: [{
                    data: Object.values(stats.emprunts_par_statut),
                    backgroundColor: ['#4ECDC4', '#FF6B6B', '#FFEAA7'],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
}

function updateRecentActivity(activities) {
    const activityList = document.getElementById('activity-list');
    if (!activityList) return;

    if (!activities || activities.length === 0) {
        activityList.innerHTML = `
            <div class="activity-item">
                <div class="activity-icon primary">
                    <i class="fas fa-info-circle"></i>
                </div>
                <div class="activity-content">
                    <div class="activity-title">Aucune activité récente</div>
                    <div class="activity-time">Les activités apparaîtront ici</div>
                </div>
            </div>
        `;
        return;
    }

    activityList.innerHTML = activities.map(activity => `
        <div class="activity-item ${activity.type || ''}">
            <div class="activity-icon ${activity.type || 'primary'}">
                ${getActivityIcon(activity.type)}
            </div>
            <div class="activity-content">
                <div class="activity-title">${activity.title}</div>
                <div class="activity-time">${activity.time}</div>
            </div>
        </div>
    `).join('');
}

function getActivityIcon(type) {
    const icons = {
        'success': '✓',
        'warning': '⚠',
        'primary': '📚',
        'info': 'ℹ'
    };
    return icons[type] || '📚';
}

function getActivityIcon(type) {
    const icons = {
        'success': '✓',
        'warning': '⚠',
        'primary': '📚'
    };
    return icons[type] || '📚';
}

function updateOccupationStats(stats) {
    const totalLivres = stats.total_livres;
    
    if (totalLivres > 0) {
        const pourcentageEmpruntes = (stats.emprunts_actifs / totalLivres * 100);
        const pourcentageDisponibles = (stats.livres_disponibles / totalLivres * 100);
        
        // Mettre à jour les barres de progression
        document.getElementById('empruntes-bar').style.width = `${pourcentageEmpruntes}%`;
        document.getElementById('disponibles-bar').style.width = `${pourcentageDisponibles}%`;
        
        // Mettre à jour les pourcentages
        document.getElementById('empruntes-percent').textContent = `${pourcentageEmpruntes.toFixed(1)}%`;
        document.getElementById('disponibles-percent').textContent = `${pourcentageDisponibles.toFixed(1)}%`;
    } else {
        document.getElementById('empruntes-percent').textContent = '0%';
        document.getElementById('disponibles-percent').textContent = '0%';
    }
}

// Actualisation automatique toutes les 30 secondes
setInterval(() => {
    fetch('/api/stats')
        .then(response => response.json())
        .then(stats => {
            updateStatsCards(stats);
            updateOccupationStats(stats); // AJOUTEZ CETTE LIGNE
            updateRecentActivity(stats.recent_activity);
        })
        .catch(error => console.error('Erreur lors de l\'actualisation:', error));
}, 30000);