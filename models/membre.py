from models.model import Model
from models.base import Base

class Membre(Model):
    __table__ = "membres"

    def __init__(self, id_membres, nom, prenom, age, email):
        self.id_membres = id_membres
        self.nom = nom
        self.prenom = prenom
        self.age = age
        self.email = email

    @classmethod
    def search(cls, search_term):
        """Recherche des membres par nom, prénom ou email"""
        try:
            # CORRECTION : Utiliser Base() au lieu de get_connection()
            base = Base()
            cursor = base.cur
            
            query = """
                SELECT * FROM membres 
                WHERE nom LIKE %s OR prenom LIKE %s OR email LIKE %s
                ORDER BY nom, prenom
            """
            search_pattern = f"%{search_term}%"
            cursor.execute(query, (search_pattern, search_pattern, search_pattern))
            
            results = cursor.fetchall()
            base.con.close()
            
            return results
        except Exception as e:
            print(f"ERREUR Membre.search: {e}")
            return []