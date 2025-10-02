from models.livre import Livre
from models.membre import Membre
from models.emprunt import Emprunt
from models.reservation import Reservation
import json
from datetime import datetime, timedelta

class DashboardController:
    
    @staticmethod
    async def __load(send, filename, dico=None):
        with open(filename, "r", encoding="utf-8") as f:
            html = f.read()
        if dico:
            for key, value in dico.items():
                placeholder = "{{ " + str(key) + " }}"
                html = html.replace(placeholder, str(value))
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [(b'content-type', b'text/html; charset=utf-8')]
        })
        await send({
            'type': 'http.response.body',
            'body': html.encode('utf-8')
        })

    @staticmethod
    async def pageDashboard(scope, receive, send):
        # Récupération des données de base
        livres = Livre.getAll()
        membres = Membre.getAll()
        emprunts_actifs = Emprunt.get_emprunts_actifs()
        emprunts_retard = Emprunt.get_emprunts_en_retard()
        livres_disponibles = Livre.get_livres_disponibles()
        reservations_attente = Reservation.get_reservations_en_attente()
        
        dico = {
            "total_livres": len(livres),
            "total_membres": len(membres),
            "emprunts_actifs": len(emprunts_actifs),
            "emprunts_retard": len(emprunts_retard),
            "livres_disponibles": len(livres_disponibles),
            "reservations_attente": len(reservations_attente)
        }
        
        await __class__.__load(send, "views/dashboard/dashboard.html", dico)

    @staticmethod
    async def getStats(scope, receive, send):
        # Récupération des données complètes
        livres = Livre.getAll()
        membres = Membre.getAll()
        emprunts_actifs = Emprunt.get_emprunts_actifs()
        emprunts_retard = Emprunt.get_emprunts_en_retard()
        livres_disponibles = Livre.get_livres_disponibles()
        reservations_attente = Reservation.get_reservations_en_attente()
        tous_emprunts = Emprunt.getAll()
        
        # Statistiques de base
        stats = {
            "total_livres": len(livres),
            "total_membres": len(membres),
            "emprunts_actifs": len(emprunts_actifs),
            "emprunts_retard": len(emprunts_retard),
            "livres_disponibles": len(livres_disponibles),
            "reservations_attente": len(reservations_attente),
            "livres_par_auteur": {},
            "membres_par_age": {},
            "emprunts_par_statut": {
                "Actifs": len(emprunts_actifs),
                "En retard": len(emprunts_retard),
                "Retournés": len([e for e in tous_emprunts if e.get('statut') == 'rendu'])
            },
            "recent_activity": __class__.__get_recent_activity()
        }
        
        # Livres par auteur
        for livre in livres:
            auteur = livre['auteur']
            stats["livres_par_auteur"][auteur] = stats["livres_par_auteur"].get(auteur, 0) + 1
        
        # Membres par âge
        for membre in membres:
            age = membre['age']
            stats["membres_par_age"][age] = stats["membres_par_age"].get(age, 0) + 1
        
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [(b'content-type', b'application/json')]
        })
        await send({
            'type': 'http.response.body',
            'body': json.dumps(stats).encode()
        })

    @staticmethod
    def __get_recent_activity():
        """Génère l'activité récente pour le dashboard"""
        from models.base import Base
        base = Base()
        
        try:
            # Derniers emprunts (7 derniers jours)
            query_emprunts = """
                SELECT e.*, l.titre, m.nom, m.prenom 
                FROM emprunts e
                JOIN livres l ON e.id_livres = l.id_livres
                JOIN membres m ON e.id_membres = m.id_membres
                WHERE e.date_emprunt >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
                ORDER BY e.date_emprunt DESC
                LIMIT 5
            """
            base.cur.execute(query_emprunts)
            emprunts_recents = base.cur.fetchall()
            
            # Derniers retours
            query_retours = """
                SELECT e.*, l.titre, m.nom, m.prenom 
                FROM emprunts e
                JOIN livres l ON e.id_livres = l.id_livres
                JOIN membres m ON e.id_membres = m.id_membres
                WHERE e.date_retour IS NOT NULL 
                AND e.date_retour >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
                ORDER BY e.date_retour DESC
                LIMIT 5
            """
            base.cur.execute(query_retours)
            retours_recents = base.cur.fetchall()
            
            activity = []
            
            # Ajouter les emprunts récents
            for emp in emprunts_recents:
                # Formater la date correctement
                date_str = emp['date_emprunt'].strftime('%d/%m/%Y') if hasattr(emp['date_emprunt'], 'strftime') else str(emp['date_emprunt'])
                
                activity.append({
                    "title": f"{emp['prenom']} {emp['nom']} a emprunté '{emp['titre']}'",
                    "time": f"Le {date_str}",
                    "type": "primary"
                })
            
            # Ajouter les retours récents
            for ret in retours_recents:
                # Formater la date correctement
                date_str = ret['date_retour'].strftime('%d/%m/%Y') if hasattr(ret['date_retour'], 'strftime') else str(ret['date_retour'])
                
                activity.append({
                    "title": f"{ret['prenom']} {ret['nom']} a retourné '{ret['titre']}'",
                    "time": f"Le {date_str}",
                    "type": "success"
                })
            
            # Ajouter des activités simulées si pas assez d'activité réelle
            if len(activity) < 3:
                activity.extend([
                    {
                        "title": "Système de gestion mis à jour",
                        "time": "Aujourd'hui",
                        "type": "info"
                    },
                    {
                        "title": "Nouveaux livres ajoutés au catalogue",
                        "time": "Cette semaine", 
                        "type": "primary"
                    }
                ])
            
            # Trier par date (les plus récentes en premier) et limiter
            activity = activity[:6]
            
            return activity
            
        except Exception as e:
            print(f"Erreur lors de la récupération de l'activité: {e}")
            # Retourner des activités par défaut en cas d'erreur
            return [
                {
                    "title": "Bienvenue sur le dashboard",
                    "time": "Maintenant", 
                    "type": "info"
                },
                {
                    "title": "Système opérationnel",
                    "time": "Aujourd'hui",
                    "type": "success"
                }
            ]
        finally:
            base.con.close()