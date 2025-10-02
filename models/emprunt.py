from models.model import Model
from datetime import datetime, timedelta

class Emprunt(Model):
    __table__ = "emprunts"

    def __init__(self, id_emprunts, id_livres, id_membres, date_emprunt, date_retour, date_retour_prevue, statut, penalite):
        self.id_emprunts = id_emprunts
        self.id_livres = id_livres
        self.id_membres = id_membres
        self.date_emprunt = date_emprunt
        self.date_retour = date_retour
        self.date_retour_prevue = date_retour_prevue
        self.statut = statut
        self.penalite = penalite

    @classmethod
    def emprunter_livre(cls, id_livre, id_membre):
        """Emprunter un livre"""
        from models.livre import Livre
        
        # Vérifier si le livre est disponible
        if not Livre.est_disponible(id_livre):
            return False, "Livre non disponible"
        
        # Vérifier si le membre a déjà ce livre
        if cls.membre_a_livre(id_membre, id_livre):
            return False, "Membre a déjà ce livre"
        
        # Vérifier si le membre peut emprunter (max 3 livres)
        if not cls.membre_peut_emprunter(id_membre):
            nb_emprunts = cls.get_nombre_emprunts_actifs(id_membre)
            return False, f"Membre a déjà {nb_emprunts}/3 livres empruntés"
        
        # Calculer les dates
        date_emprunt = datetime.now().date()
        date_retour_prevue = date_emprunt + timedelta(weeks=3)
        
        # Créer l'emprunt
        data = {
            "id_livres": id_livre,
            "id_membres": id_membre,
            "date_emprunt": date_emprunt.strftime('%Y-%m-%d'),
            "date_retour_prevue": date_retour_prevue.strftime('%Y-%m-%d'),
            "statut": "emprunté"
        }
        
        cls.insert(data)
        return True, "Emprunt réussi"

    @classmethod
    def retourner_livre(cls, id_emprunt):
        """Retourner un livre et vérifier les réservations"""
        try:
            print(f"DEBUG - Début retourner_livre ID: {id_emprunt}")
            
            emprunt = cls.getById(id_emprunt)
            print(f"DEBUG - Emprunt trouvé: {emprunt}")
            
            if not emprunt:
                print("DEBUG - Emprunt non trouvé")
                return False, "Emprunt non trouvé"
            
            date_retour = datetime.now().date()
            penalite = cls.calculer_penalite(emprunt, date_retour)
            
            data = {
                "date_retour": date_retour.strftime('%Y-%m-%d'),
                "statut": "rendu",
                "penalite": penalite
            }
            
            print(f"DEBUG - Données de mise à jour: {data}")
            
            # Utilisez la méthode update de la classe Model
            result = cls.update(id_emprunt, data)
            print(f"DEBUG - Résultat update: {result}")
            
            if result:
                print("DEBUG - Retour réussi, vérification des réservations...")
                
                # Vérifier et honorer les réservations pour ce livre
                from models.reservation import Reservation
                success, message = Reservation.verifier_et_honorer_reservations(emprunt['id_livres'])
                print(f"DEBUG - Résultat vérification réservations: {success} - {message}")
                
                return True, f"Livre retourné. Pénalité: {penalite}€. {message}"
            else:
                print("DEBUG - Échec de l'update")
                return False, "Erreur lors de la mise à jour"
                
        except Exception as e:
            print(f"ERREUR retourner_livre: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Erreur: {str(e)}"

    @classmethod
    def calculer_penalite(cls, emprunt, date_retour):
        """Calculer la pénalité pour retard"""
        try:
            # date_retour_prevue peut être soit un string soit un datetime.date
            date_prevue = emprunt['date_retour_prevue']
            
            # Si c'est une chaîne, la convertir en date
            if isinstance(date_prevue, str):
                date_prevue = datetime.strptime(date_prevue, '%Y-%m-%d').date()
            # Si c'est déjà un datetime.date, l'utiliser directement
            elif isinstance(date_prevue, datetime):
                date_prevue = date_prevue.date()
            # Si c'est déjà un date, l'utiliser directement
            # (pas besoin de conversion supplémentaire)
            
            print(f"DEBUG - Date retour prévue: {date_prevue} (type: {type(date_prevue)})")
            print(f"DEBUG - Date retour effective: {date_retour} (type: {type(date_retour)})")
            
            if date_retour <= date_prevue:
                print("DEBUG - Pas de retard")
                return 0.00
            
            jours_retard = (date_retour - date_prevue).days
            penalite = jours_retard * 0.50  # 0.50€ par jour de retard
            
            print(f"DEBUG - Jours de retard: {jours_retard}, Pénalité: {penalite}€")
            
            return min(penalite, 20.00)  # Maximum 20€
            
        except Exception as e:
            print(f"ERREUR calculer_penalite: {e}")
            return 0.00

    @classmethod
    def est_emprunte(cls, id_livre):
        """Vérifier si un livre est emprunté"""
        try:
            base = cls._get_base()
            query = "SELECT * FROM emprunts WHERE id_livres = %s AND statut = 'emprunté'"
            base.cur.execute(query, (id_livre,))
            result = base.cur.fetchone() is not None
            base.con.close()
            return result
        except Exception as e:
            print(f"Erreur est_emprunte: {e}")
            return False

    @classmethod
    def membre_a_livre(cls, id_membre, id_livre):
        """Vérifier si un membre a déjà un livre"""
        try:
            base = cls._get_base()
            query = "SELECT * FROM emprunts WHERE id_membres = %s AND id_livres = %s AND statut = 'emprunté'"
            base.cur.execute(query, (id_membre, id_livre))
            result = base.cur.fetchone() is not None
            base.con.close()
            return result
        except Exception as e:
            print(f"Erreur membre_a_livre: {e}")
            return False

    @classmethod
    def get_emprunts_actifs(cls):
        """Récupérer tous les emprunts actifs"""
        try:
            base = cls._get_base()
            query = "SELECT * FROM emprunts WHERE statut = 'emprunté'"
            base.cur.execute(query)
            result = base.cur.fetchall()
            base.con.close()
            return result
        except Exception as e:
            print(f"Erreur get_emprunts_actifs: {e}")
            return []

    @classmethod
    def get_emprunts_en_retard(cls):
        """Récupérer les emprunts en retard"""
        try:
            base = cls._get_base()
            date_aujourdhui = datetime.now().date().strftime('%Y-%m-%d')
            query = "SELECT * FROM emprunts WHERE statut = 'emprunté' AND date_retour_prevue < %s"
            base.cur.execute(query, (date_aujourdhui,))
            result = base.cur.fetchall()
            base.con.close()
            return result
        except Exception as e:
            print(f"Erreur get_emprunts_en_retard: {e}")
            return []
        
    @classmethod
    def get_emprunts_actifs_par_membre(cls, id_membre):
        """Récupérer tous les emprunts actifs d'un membre"""
        try:
            base = cls._get_base()
            query = "SELECT * FROM emprunts WHERE id_membres = %s AND statut = 'emprunté'"
            base.cur.execute(query, (id_membre,))
            result = base.cur.fetchall()
            base.con.close()
            return result
        except Exception as e:
            print(f"Erreur get_emprunts_actifs_par_membre: {e}")
            return []

    @classmethod
    def membre_peut_emprunter(cls, id_membre):
        """Vérifier si un membre peut emprunter (max 3 livres)"""
        emprunts_actifs = cls.get_emprunts_actifs_par_membre(id_membre)
        return len(emprunts_actifs) < 3

    @classmethod
    def get_nombre_emprunts_actifs(cls, id_membre):
        """Récupérer le nombre d'emprunts actifs d'un membre"""
        emprunts_actifs = cls.get_emprunts_actifs_par_membre(id_membre)
        return len(emprunts_actifs)

    @classmethod
    def _get_base(cls):
        from models.base import Base
        return Base()