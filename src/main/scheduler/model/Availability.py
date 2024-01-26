import sys
import uuid
sys.path.append("../util/*")
sys.path.append("../db/*")
from util.Util import Util
from db.ConnectionManager import ConnectionManager
import pymssql

class Availability:
    #id_iter = itertools.count()
    def __init__(self, date, username):
        self.date = date
        self.username = username

    def save_to_db(self):
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()

        add_patients = "INSERT INTO Availabilities VALUES (%s, %s)"
        try:
            cursor.execute(add_patients, (self.date, self.username))
            # you must call commit() to persist your data if you don't set autocommit to True
            conn.commit()
        except pymssql.Error:
            raise
        finally:
            cm.close_connection()
    
    def get_username(self):
        return self.username
    
    def delete_availability(self):
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()

        remove_caregiver = "DELETE FROM Availabilities WHERE Username = %s AND Time = %s"
        try:
            cursor.execute(remove_caregiver, (self.username, self.date))
            # you must call commit() to persist your data if you don't set autocommit to True
            conn.commit()
        except pymssql.Error:
            raise
        finally:
            cm.close_connection()