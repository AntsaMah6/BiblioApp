from mysql.connector import connect

class Base(object):
    def __init__(self):
        self.con = connect(
            host="localhost",
            user="root", 
            password="",
            database="biblio_db"
        )
        self.cur = self.con.cursor(dictionary=True)

    def __del__(self):
        if hasattr(self, "con") and self.con is not None:
            self.con.close()