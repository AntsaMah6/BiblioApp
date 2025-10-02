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
        if cls.membre_a_reservation(id_membre, id_livre):
            return False, "Membre a déjà réservé ce livre"
        
        data = {
            "id_livres": id_livre,
            "id_membres": id_membre,
            "statut": "en_attente"
        }
        
        cls.insert(data)
        return True, "Réservation effectuée"

    @classmethod
    def membre_a_reservation(cls, id_membre, id_livre):
        """Vérifier si un membre a réservé un livre"""
        try:
            base = cls._get_base()
            query = "SELECT * FROM reservations WHERE id_membres = %s AND id_livres = %s AND statut = 'en_attente'"
            base.cur.execute(query, (id_membre, id_livre))
            return base.cur.fetchone() is not None
        except Exception as e:
            print(f"Erreur membre_a_reservation: {e}")
            return False

    @classmethod
    def _get_base(cls):
        from models.base import Base
        return Base()