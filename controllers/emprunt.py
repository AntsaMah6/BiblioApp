from models.emprunt import Emprunt
from models.livre import Livre
from models.membre import Membre
from models.reservation import Reservation
import urllib.parse
from datetime import datetime
import json

class EmpruntController(object):

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
    async def pageEmprunts(scope, receive, send):
        """Page des emprunts actifs - Groupés par membre"""
        print("DEBUG - Début pageEmprunts")  # Debug
        
        emprunts = Emprunt.get_emprunts_actifs()
        print(f"DEBUG - Emprunts actifs trouvés: {len(emprunts)}")  # Debug
        
        # Grouper les emprunts par membre
        emprunts_par_membre = {}
        for emprunt in emprunts:
            id_membre = emprunt['id_membres']
            if id_membre not in emprunts_par_membre:
                membre = Membre.getById(id_membre)
                emprunts_par_membre[id_membre] = {
                    'membre': membre,
                    'emprunts': [],
                    'livres': []
                }
            
            livre = Livre.getById(emprunt['id_livres'])
            if livre:
                emprunts_par_membre[id_membre]['emprunts'].append(emprunt)
                emprunts_par_membre[id_membre]['livres'].append(livre)
        
        # Générer l'HTML groupé par membre
        list_emprunts = ""
        for id_membre, data in emprunts_par_membre.items():
            membre = data['membre']
            livres = data['livres']
            emprunts_list = data['emprunts']
            
            if not membre or not livres:
                continue
            
            # Date de retour la plus récente parmi tous les emprunts du membre
            dates_retour = [emp['date_retour_prevue'] for emp in emprunts_list]
            date_retour_max = max(dates_retour) if dates_retour else emprunts_list[0]['date_retour_prevue']
            
            # Liste des livres
            liste_livres = "<ul class='livres-list'>"
            for livre in livres:
                liste_livres += f"<li>{livre['titre']} - {livre['auteur']}</li>"
            liste_livres += "</ul>"
            
            # Boutons de retour (un par livre)
            boutons_retour = ""
            for emprunt in emprunts_list:
                boutons_retour += f"""
                <a href="/emprunt/retourner/{emprunt['id_emprunts']}" 
                class="btn btn-success btn-retour" 
                title="Retourner {Livre.getById(emprunt['id_livres'])['titre']}">
                Retourner {Livre.getById(emprunt['id_livres'])['titre']}
                </a>
                """
            
            list_emprunts += f"""
            <div class="carousel-item">
                <div class="item-card grouped-emprunt">
                    <div class="membre-header">
                        <h3>{membre['nom']} {membre['prenom']}</h3>
                        <span class="email">{membre['email']}</span>
                    </div>
                    
                    <div class="emprunt-details">
                        <div class="livres-section">
                            <h4>Livres empruntés ({len(livres)}) :</h4>
                            {liste_livres}
                        </div>
                        
                        <div class="dates-section">
                            <p><strong>Date d'emprunt:</strong> {emprunts_list[0]['date_emprunt']}</p>
                            <p><strong>Retour prévu le plus tardif:</strong> {date_retour_max}</p>
                        </div>
                    </div>
                    
                    <div class="item-actions grouped-actions">
                        {boutons_retour}
                    </div>
                </div>
            </div>
            """
            print(f"DEBUG - Carte générée pour membre ID: {id_membre} avec {len(livres)} livres")  # Debug
        
        dico = {"list_emprunts": list_emprunts}
        await __class__.__load(send, "views/emprunt/list_emprunt.html", dico)

    @staticmethod
    async def pageNouvelEmprunt(scope, receive, send):
        """Page pour nouveau emprunt"""
        livres_disponibles = Livre.get_livres_disponibles()
        membres = Membre.getAll()
        
        list_livres = ""
        for livre in livres_disponibles:
            list_livres += f"<option value='{livre['id_livres']}'>{livre['titre']} - {livre['auteur']}</option>"
        
        list_membres = ""
        for membre in membres:
            list_membres += f"<option value='{membre['id_membres']}'>{membre['nom']} {membre['prenom']}</option>"
        
        dico = {
            "list_livres": list_livres,
            "list_membres": list_membres
        }
        await __class__.__load(send, "views/emprunt/insert_emprunt.html", dico)

    @staticmethod
    async def opEmprunter(scope, receive, send):
        """Opération d'emprunt"""
        try:
            event = await receive()
            body = event.get("body", b"")
            dico = urllib.parse.parse_qs(body.decode())
            
            print(f"DEBUG - Données reçues: {dico}")  # Debug
            
            # Récupérer l'ID du membre
            id_membre = dico.get('id_membre', [None])[0]
            
            # Récupérer tous les IDs de livres (peut être une liste)
            id_livres = dico.get('id_livres', [])
            
            print(f"DEBUG - ID Membre: {id_membre}")  # Debug
            print(f"DEBUG - ID Livres: {id_livres}")  # Debug
            
            if not id_membre or not id_livres:
                await send({
                    'type': 'http.response.start',
                    'status': 302,
                    'headers': [(b'Location', '/emprunt/nouvel?error=Données manquantes'.encode('utf-8'))]
                })
                await send({'type': 'http.response.body', 'body': b''})
                return
            
            # Pour chaque livre, créer un emprunt
            emprunts_reussis = 0
            messages = []
            
            for id_livre in id_livres:
                success, message = Emprunt.emprunter_livre(id_livre, id_membre)
                if success:
                    emprunts_reussis += 1
                messages.append(message)
                print(f"DEBUG - Emprunt livre {id_livre}: {success} - {message}")  # Debug
            
            if emprunts_reussis > 0:
                await send({
                    'type': 'http.response.start',
                    'status': 302,
                    'headers': [(b'Location', b'/emprunt/list')]
                })
            else:
                error_message = "Aucun emprunt n'a pu être effectué: " + "; ".join(messages)
                await send({
                    'type': 'http.response.start',
                    'status': 302,
                    'headers': [(b'Location', b'/emprunt/nouvel?error=' + urllib.parse.quote(error_message))]
                })
                
        except Exception as e:
            print(f"ERREUR opEmprunter: {e}")
            await send({
                'type': 'http.response.start',
                'status': 302,
                'headers': [(b'Location', b'/emprunt/nouvel?error=Erreur serveur')]
            })
        
        await send({'type': 'http.response.body', 'body': b''})

    @staticmethod
    async def opRetourner(scope, receive, send):
        """Opération de retour"""
        try:
            # Récupérer l'ID depuis l'URL
            path = scope['path']
            id_emprunt = path.split('/')[-1]
            
            print(f"DEBUG - Retour emprunt ID: {id_emprunt}")
            
            if not id_emprunt.isdigit():
                await send({
                    'type': 'http.response.start',
                    'status': 302,
                    'headers': [(b'Location', b'/emprunt/list')]
                })
                await send({'type': 'http.response.body', 'body': b''})
                return
            
            # Appeler la méthode de retour
            success, message = Emprunt.retourner_livre(id_emprunt)
            print(f"DEBUG - Résultat retour: {success} - {message}")
            
            # TOUJOURS rediriger vers la liste des emprunts
            await send({
                'type': 'http.response.start',
                'status': 302,
                'headers': [(b'Location', b'/emprunt/list')]
            })
                
        except Exception as e:
            print(f"ERREUR opRetourner: {e}")
            await send({
                'type': 'http.response.start',
                'status': 302,
                'headers': [(b'Location', b'/emprunt/list')]
            })
        
        await send({'type': 'http.response.body', 'body': b''})

    @staticmethod
    async def pageRetards(scope, receive, send):
        """Page des retards"""
        emprunts_retard = Emprunt.get_emprunts_en_retard()
        
        # Mettre à jour le statut des retards
        for emprunt in emprunts_retard:
            Emprunt.update(emprunt['id_emprunts'], {"statut": "en_retard"})
        
        # Récupérer les détails
        retards_details = []
        for emprunt in emprunts_retard:
            livre = Livre.getById(emprunt['id_livres'])
            membre = Membre.getById(emprunt['id_membres'])
            
            if livre and membre:
                penalite = Emprunt.calculer_penalite(emprunt, datetime.now().date())
                retards_details.append({
                    'emprunt': emprunt,
                    'livre': livre,
                    'membre': membre,
                    'penalite': penalite
                })
        
        list_retards = ""
        for detail in retards_details:
            list_retards += f"""
            <div class="carousel-item">
                <div class="item-card">
                    <h3>{detail['livre']['titre']}</h3>
                    <p><strong>Auteur:</strong> {detail['livre']['auteur']}</p>
                    <p><strong>Emprunté par:</strong> {detail['membre']['nom']} {detail['membre']['prenom']}</p>
                    <p><strong>Retour prévu:</strong> {detail['emprunt']['date_retour_prevue']}</p>
                    <p><strong style="color: red;">Pénalité: {detail['penalite']}€</strong></p>
                    <div class="item-actions">
                        <a href="/emprunt/retourner/{detail['emprunt']['id_emprunts']}" 
                        class="btn btn-success btn-retour">
                        Retourner
                        </a>
                    </div>
                </div>
            </div>
            """
        dico = {"list_retards": list_retards}
        await __class__.__load(send, "views/emprunt/retard.html", dico)

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