from models.livre import Livre
import urllib.parse
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
            list_livre += f"""
            <div class="carousel-item">
                <div class="item-card">
                    <h3>{livre['titre']}</h3>
                    <p><strong>Auteur:</strong> {livre['auteur']}</p>
                    <div class="item-actions">
                        <a href="/livre/update/{livre['id_livres']}" class="btn btn-primary">Modifier</a>
                        <button class="btn btn-danger btn-suppr" data-id="{livre['id_livres']}">Supprimer</button>
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