from models.membre import Membre
import urllib.parse
import json

class MembreController(object):
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
    async def pageList(scope, receive, send):
        membres = Membre.getAll()
        list_membre = ""
        
        for i, membre in enumerate(membres):
            list_membre += f"""
            <div class="carousel-item">
                <div class="item-card">
                    <h3>{membre['nom']} {membre['prenom']}</h3>
                    <p><strong>Âge:</strong> {membre['age']} ans</p>
                    <p><strong>Email:</strong> {membre['email']}</p>
                    <div class="item-actions">
                        <a href="/membre/update/{membre['id_membres']}" class="btn btn-primary">Modifier</a>
                        <button class="btn btn-danger btn-suppr" data-id="{membre['id_membres']}">Supprimer</button>
                    </div>
                </div>
            </div>
            """
        
        dico = {"list_membre": list_membre}
        await __class__.__load(send, "views/membre/list_membre.html", dico)

    @staticmethod
    async def pageInsert(scope, receive, send):
        dico = {
            "form_title": "Ajouter un membre",
            "form_action": "/membre/insert/opinsert",
            "button_text": "Ajouter",
            "id_membre": "",
            "nom": "",
            "prenom": "", 
            "age": "",
            "email": ""
        }
        await __class__.__load(send, "views/membre/insert_membre.html", dico)

    @staticmethod
    async def opInsert(scope, receive, send):
        event = await receive()
        body = event.get("body", b'')
        dico = urllib.parse.parse_qs(body.decode())
        dico = {k: v[0] for k, v in dico.items()}
        
        Membre.insert(dico)
        
        # Rediriger vers la liste des membres
        await send({
            'type': 'http.response.start',
            'status': 302,
            'headers': [(b'Location', b'/membre/list')]
        })
        await send({
            'type': 'http.response.body',
            'body': b''
        })

    @staticmethod
    async def pageUpdate(scope, receive, send):
        try:
            # Récupérer l'id depuis l'URL
            path = scope['path']
            id = path.split('/')[-1]
            
            print(f"DEBUG - ID membre reçu: {id}")  
            
            membre = Membre.getById(id)
            print(f"DEBUG - Données membre: {membre}") 
            
            if not membre:
                await __class__.error404(scope, receive, send)
                return
            
            dico = {
                "form_title": "Modifier un membre",
                "form_action": "/membre/update/opupdate", 
                "button_text": "Modifier",
                "id_membre": membre["id_membres"],
                "nom": membre["nom"],
                "prenom": membre["prenom"],
                "age": membre["age"],
                "email": membre["email"]
            }
            await __class__.__load(send, "views/membre/insert_membre.html", dico)
        except Exception as e:
            print(f"ERREUR pageUpdate membre: {e}")
            await __class__.error404(scope, receive, send)

    @staticmethod
    async def opUpdate(scope, receive, send):
        event = await receive()
        body = event.get("body", b'')
        dico = urllib.parse.parse_qs(body.decode())
        dico = {k: v[0] for k, v in dico.items()}
        Membre.update(dico["id_membres"], dico)
        await send({
            'type': 'http.response.start',
            'status': 302,
            'headers': [(b'Location', b'/membre/list')]
        })
        await send({
            'type': 'http.response.body',
            'body': b''
        })

    @staticmethod
    async def opDelete(scope, receive, send):
        id = scope['path'].split('/')[-1]
        Membre.delete(id)
        await send({
            'type': 'http.response.start',
            'status': 302,
            'headers': [(b'Location', b'/membre/list')]
        })
        await send({
            'type': 'http.response.body',
            'body': b''
        })

    @staticmethod
    async def apiMembres(scope, receive, send):
        """API pour tous les membres avec nombre d'emprunts"""
        from models.emprunt import Emprunt
        
        membres = Membre.getAll()
        
        # Ajouter le nombre d'emprunts actifs pour chaque membre
        membres_avec_emprunts = []
        for membre in membres:
            nb_emprunts = Emprunt.get_nombre_emprunts_actifs(membre['id_membres'])
            membre['emprunts_actifs'] = nb_emprunts
            membres_avec_emprunts.append(membre)
        
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [(b'content-type', b'application/json')]
        })
        await send({
            'type': 'http.response.body',
            'body': json.dumps(membres_avec_emprunts).encode()
        })
    
    @staticmethod
    async def searchMembres(scope, receive, send):
        """API de recherche de membres"""
        try:
            # Récupérer le terme de recherche depuis les paramètres GET
            query_string = scope.get('query_string', b'').decode()
            params = urllib.parse.parse_qs(query_string)
            search_term = params.get('q', [''])[0]
            
            print(f"DEBUG - Recherche de membres avec le terme: {search_term}")
            
            if search_term:
                membres = Membre.search(search_term)
            else:
                membres = Membre.getAll()
            
            print(f"DEBUG - {len(membres)} membres trouvés")
            
            # Retourner les résultats en JSON
            await send({
                'type': 'http.response.start',
                'status': 200,
                'headers': [(b'content-type', b'application/json')]
            })
            await send({
                'type': 'http.response.body',
                'body': json.dumps(membres).encode()
            })
        except Exception as e:
            print(f"ERREUR searchMembres: {e}")
            await send({
                'type': 'http.response.start',
                'status': 500,
                'headers': [(b'content-type', b'application/json')]
            })
            await send({
                'type': 'http.response.body',
                'body': json.dumps({"error": "Erreur lors de la recherche"}).encode()
            })