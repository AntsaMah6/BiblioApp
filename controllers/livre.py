from models.livre import Livre
import urllib.parse
from models.reservation import Reservation
import json

class LivreController(object):

    @staticmethod
    async def __load(send, filename, dico=None):
        with open(filename, "r", encoding="utf-8") as f:
            html = f.read()

        if dico:
            for key, value in dico.items():
                placeholder = "{{ " + str(key) + " }}"
                html = html.replace(placeholder, str(value))

        await send({
            'type' : 'http.response.start',
            'status' : 200,
            'headers' : [(b'content-type' , b'text/html; charset=utf-8')]
        })

        await send({
            'type' : 'http.response.body',
            'body' : html.encode('utf-8')
        })

    @staticmethod
    async def pageList(scope, receive, send):
        
        livres = Livre.getAll()
        list_livre = ""
        
        for livre in livres:
            # Vérifier si le livre est disponible
            est_disponible = Livre.est_disponible(livre['id_livres'])
            
            # Récupérer le nombre de réservations pour ce livre
            reservations = Reservation.get_reservations_par_livre(livre['id_livres'])
            nb_reservations = len(reservations)
            
            # Déterminer l'affichage du statut
            statut_html = ""
            if est_disponible:
                statut_html = "<span style='color: green;'>✓ Disponible</span>"
            else:
                if nb_reservations > 0:
                    statut_html = f"<span style='color: orange;'>✗ Emprunté ({nb_reservations} réservation(s))</span>"
                else:
                    statut_html = "<span style='color: red;'>✗ Emprunté</span>"
            
            # Générer le bouton de réservation conditionnel
            bouton_reservation = ""
            if not est_disponible:
                bouton_reservation = f'<a href="/reservation/nouvel?id_livre={livre["id_livres"]}" class="btn btn-warning">Réserver</a>'
            
            # CORRECTION : Utiliser des liens au lieu de boutons avec data-id
            list_livre += f"""
            <div class="carousel-item">
                <div class="item-card">
                    <h3>{livre['titre']}</h3>
                    <p><strong>Auteur:</strong> {livre['auteur']}</p>
                    <p><strong>Statut:</strong> {statut_html}</p>
                    <div class="item-actions">
                        <a href="/livre/update/{livre['id_livres']}" class="btn btn-primary">Modifier</a>
                        <a href="/livre/delete/{livre['id_livres']}" class="btn btn-danger">Supprimer</a>
                        {bouton_reservation}
                    </div>
                </div>
            </div>
            """
        
        dico = {"list_livre": list_livre}
        await __class__.__load(send, "views/livre/list_livre.html", dico)

    @staticmethod
    async def pageInsert(scope, receive, send):
        dico = {
            "form_title": "Ajouter un livre",
            "form_action": "/livre/insert/opinsert",
            "button_text": "Ajouter",
            "id_livre": "",
            "titre": "",
            "auteur": ""
        }
        await __class__.__load(send, "views/livre/insert_livre.html", dico)

    @staticmethod
    async def pageUpdate(scope, receive, send):
        try:
            # Récupérer l'id depuis l'URL
            path = scope['path']
            id = path.split('/')[-1]
            
            print(f"DEBUG - ID reçu: {id}")  
            
            livre = Livre.getById(id)
            print(f"DEBUG - Données livre: {livre}")  
            
            if not livre:
                await __class__.error404(scope, receive, send)
                return
            
            dico = {
                "form_title": "Modifier un livre",
                "form_action": "/livre/update/opupdate",
                "button_text": "Modifier",
                "id_livre": livre["id_livres"],
                "titre": livre["titre"],
                "auteur": livre["auteur"]
            }
            await __class__.__load(send, "views/livre/insert_livre.html", dico)
        except Exception as e:
            print(f"ERREUR pageUpdate: {e}")
            await __class__.error404(scope, receive, send)

    @staticmethod
    async def error404(scope, receive, send):
        await __class__.__load(send, "views/error404.html")

    @staticmethod
    async def opInsert(scope, receive, send):
        event = await receive()
        body = event.get("body", b"")
        dico = urllib.parse.parse_qs(body.decode())
        dico = {k: v[0] for k, v in dico.items()}
        
        Livre.insert(dico)
        
        # Rediriger vers la liste des livres
        await send({
            'type': 'http.response.start',
            'status': 302,
            'headers': [(b'Location', b'/livre/list')]
        })
        await send({
            'type': 'http.response.body',
            'body': b''
        })

    @staticmethod
    async def opUpdate(scope, receive, send):
        event = await receive()
        body = event.get("body", b"")
        dico = urllib.parse.parse_qs(body.decode())
        dico = {k: v[0] for k, v in dico.items()}
        Livre.update(dico["id_livres"], dico)
        await send({
            'type': 'http.response.start',
            'status': 302,
            'headers': [(b'Location', b'/livre/list')]
        })
        await send({
            'type': 'http.response.body',
            'body': b''
        })

    @staticmethod
    async def opDelete(scope, receive, send):
        id = scope['path'].split('/')[-1]
        Livre.delete(id)
        await send({
            'type': 'http.response.start',
            'status': 302,
            'headers': [(b'Location', b'/livre/list')]
        })
        await send({
            'type': 'http.response.body',
            'body': b''
        })

    @staticmethod
    async def apiLivresDisponibles(scope, receive, send):
        """API pour livres disponibles"""
        livres = Livre.get_livres_disponibles()
        
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [(b'content-type', b'application/json')]
        })
        await send({
            'type': 'http.response.body',
            'body': json.dumps(livres).encode()
        })

    @staticmethod
    async def searchLivres(scope, receive, send):
        """API de recherche de livres"""
        try:
            # Récupérer le terme de recherche depuis les paramètres GET
            query_string = scope.get('query_string', b'').decode()
            params = urllib.parse.parse_qs(query_string)
            search_term = params.get('q', [''])[0]
            
            if search_term:
                livres = Livre.search(search_term)
            else:
                livres = Livre.getAll()
            
            # Retourner les résultats en JSON
            await send({
                'type': 'http.response.start',
                'status': 200,
                'headers': [(b'content-type', b'application/json')]
            })
            await send({
                'type': 'http.response.body',
                'body': json.dumps(livres).encode()
            })
        except Exception as e:
            print(f"ERREUR searchLivres: {e}")
            await send({
                'type': 'http.response.start',
                'status': 500,
                'headers': [(b'content-type', b'application/json')]
            })
            await send({
                'type': 'http.response.body',
                'body': json.dumps({"error": "Erreur lors de la recherche"}).encode()
            })

    @staticmethod
    async def apiLivresEmpruntes(scope, receive, send):
        """API pour livres actuellement empruntés"""
        try:
            from models.base import Base
            
            print("DEBUG - API livres empruntés appelée")
            
            base = Base()
            query = """
                SELECT l.*, e.date_retour_prevue, e.date_emprunt, e.id_emprunts 
                FROM livres l 
                INNER JOIN emprunts e ON l.id_livres = e.id_livres 
                WHERE e.statut = 'emprunté'
                ORDER BY l.titre
            """
            base.cur.execute(query)
            livres_empruntes = base.cur.fetchall()
            base.con.close()
            
            print(f"DEBUG - {len(livres_empruntes)} livres empruntés trouvés via requête directe")
            
            # Formater les données pour inclure les informations d'emprunt
            result = []
            for livre in livres_empruntes:
                # Convertir les dates en strings pour la sérialisation JSON
                date_retour_prevue = livre['date_retour_prevue']
                date_emprunt = livre['date_emprunt']
                
                # Si ce sont des objets date, les convertir en string
                if hasattr(date_retour_prevue, 'strftime'):
                    date_retour_prevue = date_retour_prevue.strftime('%Y-%m-%d')
                if hasattr(date_emprunt, 'strftime'):
                    date_emprunt = date_emprunt.strftime('%Y-%m-%d')
                
                result.append({
                    'id_livres': livre['id_livres'],
                    'titre': livre['titre'],
                    'auteur': livre['auteur'],
                    'emprunt': {
                        'date_retour_prevue': date_retour_prevue,
                        'date_emprunt': date_emprunt,
                        'id_emprunts': livre['id_emprunts']
                    }
                })
            
            # CORRECTION : Envoyer d'abord le start, puis le body
            await send({
                'type': 'http.response.start',
                'status': 200,
                'headers': [(b'content-type', b'application/json')]
            })
            await send({
                'type': 'http.response.body',
                'body': json.dumps(result).encode()
            })
            
        except Exception as e:
            print(f"ERREUR apiLivresEmpruntes: {e}")
            import traceback
            traceback.print_exc()
            
            # CORRECTION : Envoyer d'abord le start, puis le body pour les erreurs aussi
            await send({
                'type': 'http.response.start',
                'status': 500,
                'headers': [(b'content-type', b'application/json')]
            })
            await send({
                'type': 'http.response.body',
                'body': json.dumps({"error": str(e)}).encode()
            })