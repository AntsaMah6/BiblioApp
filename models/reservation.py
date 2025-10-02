
from models.model import Model
from datetime import datetime

class Reservation(Model):
    __table__ = "reservations"

    def __init__(self, id_reservation, id_livres, id_membres, date_reservation, statut):
        self.id_reservation = id_reservation
        self.id_livres = id_livres
        self.id_membres = id_membres
        self.date_reservation = date_reservation
        self.statut = statut

    @classmethod
    def reserver_livre(cls, id_livre, id_membre):
        """Réserver un livre"""
        from models.livre import Livre
        from models.emprunt import Emprunt
        
        # Vérifier si le livre existe
        livre = Livre.getById(id_livre)
        if not livre:
            return False, "Livre non trouvé"
        
        # Vérifier si le livre est disponible
        if Livre.est_disponible(id_livre):
            return False, "Livre disponible, pas besoin de réservation"
        
        # Vérifier si le membre a déjà réservé ce livre
        if cls.membre_a_reservation_active(id_membre, id_livre):
            return False, "Membre a déjà réservé ce livre"
        
        # Vérifier si le membre a déjà emprunté ce livre
        if Emprunt.membre_a_livre(id_membre, id_livre):
            return False, "Membre a déjà emprunté ce livre"
        
        data = {
            "id_livres": id_livre,
            "id_membres": id_membre,
            "statut": "en_attente"
        }
        
        cls.insert(data)
        return True, "Réservation effectuée"

    @classmethod
    def membre_a_reservation_active(cls, id_membre, id_livre):
        """Vérifier si un membre a une réservation active pour un livre"""
        try:
            base = cls._get_base()
            query = "SELECT * FROM reservations WHERE id_membres = %s AND id_livres = %s AND statut = 'en_attente'"
            base.cur.execute(query, (id_membre, id_livre))
            return base.cur.fetchone() is not None
        except Exception as e:
            print(f"Erreur membre_a_reservation_active: {e}")
            return False

    @classmethod
    def get_reservations_en_attente(cls):
        """Récupérer toutes les réservations en attente"""
        try:
            base = cls._get_base()
            query = "SELECT * FROM reservations WHERE statut = 'en_attente' ORDER BY date_reservation"
            base.cur.execute(query)
            result = base.cur.fetchall()
            base.con.close()
            return result
        except Exception as e:
            print(f"Erreur get_reservations_en_attente: {e}")
            return []

    @classmethod
    def get_reservations_par_livre(cls, id_livre):
        """Récupérer les réservations pour un livre spécifique"""
        try:
            base = cls._get_base()
            query = "SELECT * FROM reservations WHERE id_livres = %s AND statut = 'en_attente' ORDER BY date_reservation"
            base.cur.execute(query, (id_livre,))
            result = base.cur.fetchall()
            base.con.close()
            return result
        except Exception as e:
            print(f"Erreur get_reservations_par_livre: {e}")
            return []

    @classmethod
    def get_premiere_reservation(cls, id_livre):
        """Récupérer la première réservation pour un livre"""
        reservations = cls.get_reservations_par_livre(id_livre)
        return reservations[0] if reservations else None

    @classmethod
    def honorer_reservation(cls, id_reservation):
        """Honorer une réservation (la transformer en emprunt)"""
        try:
            reservation = cls.getById(id_reservation)
            if not reservation:
                return False, "Réservation non trouvée"
            
            # Créer l'emprunt
            from models.emprunt import Emprunt
            success, message = Emprunt.emprunter_livre(reservation['id_livres'], reservation['id_membres'])
            
            if success:
                # Marquer la réservation comme honorée
                cls.update(id_reservation, {"statut": "honorée"})
                return True, "Réservation honorée avec succès"
            else:
                return False, f"Impossible d'honorer la réservation: {message}"
                
        except Exception as e:
            print(f"ERREUR honorer_reservation: {e}")
            return False, f"Erreur: {str(e)}"

    @classmethod
    def annuler_reservation(cls, id_reservation):
        """Annuler une réservation"""
        try:
            cls.update(id_reservation, {"statut": "annulée"})
            return True, "Réservation annulée"
        except Exception as e:
            print(f"ERREUR annuler_reservation: {e}")
            return False, f"Erreur: {str(e)}"

    @classmethod
    def verifier_et_honorer_reservations(cls, id_livre):
        """Vérifier et honorer automatiquement les réservations quand un livre est retourné"""
        try:
            # Récupérer la première réservation en attente pour ce livre
            reservation = cls.get_premiere_reservation(id_livre)
            
            if reservation:
                # Honorer automatiquement la réservation
                return cls.honorer_reservation(reservation['id_reservation'])
            
            return False, "Aucune réservation à honorer"
        except Exception as e:
            print(f"ERREUR verifier_et_honorer_reservations: {e}")
            return False, f"Erreur: {str(e)}"

    @classmethod
    def _get_base(cls):
        from models.base import Base
        return Base()