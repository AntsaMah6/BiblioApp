from models.model import Model

class Auth(Model):
    __table__ = "auth"

    def __init__(self, id_auth, username, password):
        self.username = username
        self.password = password
        self.id_auth = id_auth

    @classmethod
    def getByUsernameAndPassword(cls, username, password):
        try:
            # Import ici pour éviter les dépendances circulaires
            from models.base import Base
            base = Base()
            query = "SELECT * FROM auth WHERE username = %s AND password = %s"
            base.cur.execute(query, (username, password))
            user = base.cur.fetchone()
            # Ne pas fermer la connexion ici, car elle est gérée par le modèle de base
            return user
        except Exception as e:
            print(f"Erreur lors de la récupération de l'utilisateur: {e}")
            return None