from models.base import Base

class Model(object):
    def __str__(self) :
        chaine = "......................\n\n"
        for attr in self.__dict__.keys():
            chaine = chaine + f"{attr:11s}" + ":" + str(self.__dict__[attr]) +"\n"
        return chaine


    @classmethod
    def getAll(cls):
        try:
            base = Base()  # Nouvelle connexion à chaque fois
            table = getattr(cls, "__table__", cls.__name__.lower())
            query = f"SELECT * FROM {table}"
            base.cur.execute(query)
            listDict = base.cur.fetchall()
            base.con.close()  # Fermer la connexion
            return listDict
        except Exception as e:
            print(f"Erreur getAll {cls.__name__}: {e}")
            return []

    @classmethod
    def getById(cls, id):
        try:
            base = Base()  # Nouvelle connexion à chaque fois
            table = getattr(cls, "__table__", cls.__name__.lower())
            pk = "id_" + table
            query = f"SELECT * FROM {table} WHERE {pk} = %s"    
            base.cur.execute(query, (id,))
            result = base.cur.fetchone()
            base.con.close()  # Fermer la connexion
            return result
        except Exception as e:
            print(f"Erreur getById {cls.__name__}: {e}")
            return None

    @classmethod
    def insert(cls, data):
        try:
            base = cls._get_base()
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            query = f"INSERT INTO {cls.__table__} ({columns}) VALUES ({placeholders})"
            
            print(f"DEBUG Model.insert - Query: {query}")  # Debug
            print(f"DEBUG Model.insert - Values: {list(data.values())}")  # Debug
            
            base.cur.execute(query, list(data.values()))
            base.con.commit()
            result = base.cur.lastrowid
            base.con.close()
            
            print(f"DEBUG Model.insert - ID inséré: {result}")  # Debug
            return result
        except Exception as e:
            print(f"ERREUR Model.insert: {e}")  # Debug
            return False

    @classmethod
    def save(cls, *params):
        try:
            table = getattr(cls, "__table__", cls.__name__.lower())
            param = ", ".join(["%s"] * len(params))
            query = f"INSERT INTO {table} VALUES (NULL, {param})"
            base = Base()
            base.cur.execute(query, params)
        except Exception as e :
            print(e)
            return {}
        else:
            return base.con.commit()
       

    @classmethod
    def delete(cls, id):
        try:
            base = Base()  # Nouvelle connexion à chaque fois
            table = getattr(cls, "__table__", cls.__name__.lower())
            pk = "id_" + table
            query = f"DELETE FROM {table} WHERE {pk} = %s"    
            base.cur.execute(query, (id,))
            base.con.commit()
            base.con.close()  # Fermer la connexion
            return True
        except Exception as e:
            print(f"Erreur delete {cls.__name__}: {e}")
            return False

    @classmethod
    def update(cls, id, data:dict):
        try:
            base = Base()  # Nouvelle connexion à chaque fois
            table = getattr(cls, "__table__", cls.__name__.lower())
            pk = "id_" + table

            set_clause = ", ".join([f"{k} = %s" for k in data.keys()])
            query = f"UPDATE {table} SET {set_clause} WHERE {pk} = %s"

            valeurs = list(data.values()) + [id]
            base.cur.execute(query, valeurs)
            base.con.commit()
            base.con.close()  # Fermer la connexion
            return base.cur.rowcount 
        except Exception as e:
            print(f"Erreur update {cls.__name__}: {e}")
            return 0

    @classmethod
    def lastId(cls):
        return 0