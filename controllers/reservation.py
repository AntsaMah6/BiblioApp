# controllers/reservation.py
from models.reservation import Reservation
from models.livre import Livre
from models.membre import Membre
import urllib.parse
import json

class ReservationController(object):

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
        """Page des réservations en attente"""
        reservations = Reservation.get_reservations_en_attente()
        
        list_reservations = ""
        for reservation in reservations:
            livre = Livre.getById(reservation['id_livres'])
            membre = Membre.getById(reservation['id_membres'])
            
            if livre and membre:
                # CORRECTION : Utiliser des liens au lieu de boutons avec data-id
                list_reservations += f"""
                <div class="carousel-item">
                    <div class="item-card">
                        <h3>{livre['titre']}</h3>
                        <p><strong>Auteur:</strong> {livre['auteur']}</p>
                        <p><strong>Réservé par:</strong> {membre['nom']} {membre['prenom']}</p>
                        <p><strong>Email:</strong> {membre['email']}</p>
                        <p><strong>Date réservation:</strong> {reservation['date_reservation']}</p>
                        <div class="item-actions">
                            <a href="/reservation/honorer/{reservation['id_reservation']}" class="btn btn-success">
                                Honorer la réservation
                            </a>
                            <a href="/reservation/annuler/{reservation['id_reservation']}" class="btn btn-danger">
                                Annuler
                            </a>
                        </div>
                    </div>
                </div>
                """
        
        dico = {"list_reservations": list_reservations}
        await __class__.__load(send, "views/reservation/list_reservation.html", dico)

    @staticmethod
    async def opReserver(scope, receive, send):
        """Opération de réservation"""
        try:
            event = await receive()
            body = event.get("body", b"")
            dico = urllib.parse.parse_qs(body.decode())
            
            id_livre = dico.get('id_livre', [None])[0]
            id_membre = dico.get('id_membre', [None])[0]
            
            if not id_livre or not id_membre:
                await send({
                    'type': 'http.response.start',
                    'status': 302,
                    'headers': [(b'Location', '/reservation/nouvel?error=Données manquantes'.encode('utf-8'))]
                })
                await send({'type': 'http.response.body', 'body': b''})
                return
            
            success, message = Reservation.reserver_livre(id_livre, id_membre)
            
            if success:
                await send({
                    'type': 'http.response.start',
                    'status': 302,
                    'headers': [(b'Location', b'/reservation/list')]
                })
            else:
                await send({
                    'type': 'http.response.start',
                    'status': 302,
                    'headers': [(b'Location', b'/reservation/nouvel?error=' + urllib.parse.quote(message))]
                })
                
        except Exception as e:
            print(f"ERREUR opReserver: {e}")
            await send({
                'type': 'http.response.start',
                'status': 302,
                'headers': [(b'Location', b'/reservation/nouvel?error=Erreur serveur')]
            })
        
        await send({'type': 'http.response.body', 'body': b''})

    @staticmethod
    async def opHonorer(scope, receive, send):
        """Honorer une réservation"""
        try:
            path = scope['path']
            id_reservation = path.split('/')[-1]
            
            success, message = Reservation.honorer_reservation(id_reservation)
            
            if success:
                await send({
                    'type': 'http.response.start',
                    'status': 302,
                    'headers': [(b'Location', b'/reservation/list')]
                })
            else:
                await send({
                    'type': 'http.response.start',
                    'status': 302,
                    'headers': [(b'Location', b'/reservation/list?error=' + urllib.parse.quote(message))]
                })
                
        except Exception as e:
            print(f"ERREUR opHonorer: {e}")
            await send({
                'type': 'http.response.start',
                'status': 302,
                'headers': [(b'Location', b'/reservation/list?error=Erreur serveur')]
            })
        
        await send({'type': 'http.response.body', 'body': b''})

    @staticmethod
    async def opAnnuler(scope, receive, send):
        """Annuler une réservation"""
        try:
            path = scope['path']
            id_reservation = path.split('/')[-1]
            
            success, message = Reservation.annuler_reservation(id_reservation)
            
            await send({
                'type': 'http.response.start',
                'status': 302,
                'headers': [(b'Location', b'/reservation/list')]
            })
                
        except Exception as e:
            print(f"ERREUR opAnnuler: {e}")
            await send({
                'type': 'http.response.start',
                'status': 302,
                'headers': [(b'Location', b'/reservation/list?error=Erreur serveur')]
            })
        
        await send({'type': 'http.response.body', 'body': b''})

    @staticmethod
    async def pageNouvelleReservation(scope, receive, send):
        """Page pour nouvelle réservation"""
        livres_non_disponibles = [livre for livre in Livre.getAll() if not Livre.est_disponible(livre['id_livres'])]
        membres = Membre.getAll()
        
        list_livres = ""
        for livre in livres_non_disponibles:
            list_livres += f"<option value='{livre['id_livres']}'>{livre['titre']} - {livre['auteur']} (Indisponible)</option>"
        
        list_membres = ""
        for membre in membres:
            list_membres += f"<option value='{membre['id_membres']}'>{membre['nom']} {membre['prenom']}</option>"
        
        dico = {
            "list_livres": list_livres,
            "list_membres": list_membres
        }
        await __class__.__load(send, "views/reservation/insert_reservation.html", dico)