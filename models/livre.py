from models.model import Model

class Livre(Model):
    __table__ = "livres"

    def __init__(self, id_livres, titre, auteur):
        self.titre = titre
        self.auteur = auteur
        self.id_livres = id_livres

    @classmethod
    def est_disponible(cls, id_livre):
        """Vérifier si un livre est disponible"""
        from models.emprunt import Emprunt
        return not Emprunt.est_emprunte(id_livre)

    @classmethod
    def get_livres_disponibles(cls):
        """Récupérer tous les livres disponibles"""
        livres = cls.getAll()
        disponibles = []
        
        for livre in livres:
            if cls.est_disponible(livre['id_livres']):
                disponibles.append(livre)
        
        return disponibles

    @classmethod
    def get_livres_empruntes(cls):
        """Récupérer tous les livres empruntés"""
        from models.emprunt import Emprunt
        
        emprunts = Emprunt.get_emprunts_actifs()
        livres_empruntes = []
        
        for emprunt in emprunts:
            livre = cls.getById(emprunt['id_livres'])
            if livre:
                livre['emprunt'] = emprunt
                livres_empruntes.append(livre)
        
        return livres_empruntes
    
    @classmethod
    def search(cls, search_term):
        """Recherche des livres par titre ou auteur"""
        conn = cls.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT * FROM livres 
            WHERE titre LIKE %s OR auteur LIKE %s
            ORDER BY titre
        """
        search_pattern = f"%{search_term}%"
        cursor.execute(query, (search_pattern, search_pattern))
        
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return results