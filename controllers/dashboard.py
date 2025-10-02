from models.livre import Livre
from models.membre import Membre
import json

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
        livres = Livre.getAll()
        membres = Membre.getAll()
        from models.emprunt import Emprunt
        emprunts_actifs = Emprunt.get_emprunts_actifs()
        emprunts_retard = Emprunt.get_emprunts_en_retard()
        
        dico = {
            "total_livres": len(livres),
            "total_membres": len(membres),
            "emprunts_actifs": len(emprunts_actifs),
            "emprunts_retard": len(emprunts_retard)
        }
        
        await __class__.__load(send, "views/dashboard/dashboard.html", dico)

    @staticmethod
    async def getStats(scope, receive, send):
        livres = Livre.getAll()
        membres = Membre.getAll()
        from models.emprunt import Emprunt
        emprunts_actifs = Emprunt.get_emprunts_actifs()
        emprunts_retard = Emprunt.get_emprunts_en_retard()
        
        stats = {
            "total_livres": len(livres),
            "total_membres": len(membres),
            "emprunts_actifs": len(emprunts_actifs),
            "emprunts_retard": len(emprunts_retard),
            "livres_par_auteur": {},
            "membres_par_age": {}
        }
        
        for livre in livres:
            auteur = livre['auteur']
            stats["livres_par_auteur"][auteur] = stats["livres_par_auteur"].get(auteur, 0) + 1
        
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