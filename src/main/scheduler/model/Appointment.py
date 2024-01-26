import sys
import uuid
sys.path.append("../util/*")
sys.path.append("../db/*")
from util.Util import Util
from db.ConnectionManager import ConnectionManager
import pymssql

class Appointment:
    #id_iter = itertools.count()
    def __init__(self, caregiver_name, patient_name, date, vaccine_name):
        self.appointment_ID = uuid.uuid4() #next(self.id_iter) #
        self.caregiver = caregiver_name
        self.patient = patient_name
        self.date = date
        self.vaccine = vaccine_name

    def save_to_db(self):
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()

        add_patients = "INSERT INTO Appointments VALUES (%s, %s, %s, %s, %s)"
        try:
            #print("insert try")
            cursor.execute(add_patients, (self.appointment_ID, self.caregiver, self.patient, self.date, self.vaccine))
            # you must call commit() to persist your data if you don't set autocommit to True
            conn.commit()
        except pymssql.Error:
            raise
        finally:
            cm.close_connection()
    
    def get_appointmentID(self):
        return self.appointment_ID
    
    def get_appointment(self, AppointmentID):
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor(as_dict=True)

        get_apt_details = "SELECT * FROM Appointments WHERE AppointmentID = %s"
        try:
            cursor.execute(get_apt_details, AppointmentID)
            for row in cursor:
                self.caregiver = row['Caregivername']
                self.patient = row['Patientname']
                self.date = row['Time']
                self.vaccine = row['Vaccinename']
                
        except pymssql.Error as e:
            print("Error occurred when fetching current caregiver")
            raise e
        finally:
            cm.close_connection()
        return []
            
    