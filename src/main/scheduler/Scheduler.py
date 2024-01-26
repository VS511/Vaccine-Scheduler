from model.Vaccine import Vaccine
from model.Caregiver import Caregiver
from model.Patient import Patient
from model.Appointment import Appointment
from model.Availability import Availability
from util.Util import Util
from db.ConnectionManager import ConnectionManager
import pymssql
import datetime
import random


'''
objects to keep track of the currently logged-in user
Note: it is always true that at most one of currentCaregiver and currentPatient is not null
        since only one user can be logged-in at a time
'''
current_patient = None
current_caregiver = None

def password_check(passwd):

    special_characters =['!', '@', '#', '?']
    val = True

    if len(passwd) < 8:
        print('Password length should be at least 8 characters')
        val = False

    if not any(char.isdigit() for char in passwd):
        print('Password should have at least one number')
        val = False

    if not any(char.isupper() for char in passwd):
        print('Password should have at least one uppercase letter')
        val = False

    if not any(char.islower() for char in passwd):
        print('Password should have at least one lowercase letter')
        val = False

    if not any(char in special_characters for char in passwd):
        print('Password should have at least one of the symbols: ! @ # ?')
        val = False

    if val:
        return True


def create_patient(tokens):
    # create_caregiver <username> <password>
    # check 1: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again! This command requires 2 arguments <username>, <password>, in addition to create_patient function name.")
        return

    username = tokens[1]
    password = tokens[2]

    # check 2: check if the username has been taken already
    if username_exists_patient(username):
        print("Username taken, try again!")
        return

    if password_check(password):
        salt = Util.generate_salt()
        hash = Util.generate_hash(password, salt)

        # create the patient
        patient = Patient(username, salt=salt, hash=hash)

        # save to caregiver information to our database
        try:
            patient.save_to_db()
        except pymssql.Error as e:
            print("Create caregiver failed, Cannot save")
            print("Db-Error:", e)
            return
        except Exception as e:
            print("Error:", e)
            return
        print(" *** Account created successfully *** ")

    else:
        print('Please create a strong password with the above guidelines and try again.')
        return

def username_exists_patient(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Patients WHERE Username = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_username, username)
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['Username'] is not None
    except pymssql.Error as e:
        print("Error occurred when checking username")
        print("Db-Error:", e)
        return
    except Exception as e:
        print("Error:", e)
    finally:
        cm.close_connection()
    return False


def create_caregiver(tokens):
    # create_caregiver <username> <password>
    # check 1: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again! This command requires 2 arguments <username>, <password>, in addition to create_caregiver function name.")
        return

    username = tokens[1]
    password = tokens[2]
    # check 2: check if the username has been taken already
    if username_exists_caregiver(username):
        print("Username taken, try again!")
        return

    if password_check(password):
        salt = Util.generate_salt()
        hash = Util.generate_hash(password, salt)

        # create the caregiver
        caregiver = Caregiver(username, salt=salt, hash=hash)

        # save to caregiver information to our database
        try:
            caregiver.save_to_db()
        except pymssql.Error as e:
            print("Create caregiver failed, Cannot save")
            print("Db-Error:", e)
            return
        except Exception as e:
            print("Error:", e)
            return
        print(" *** Account created successfully *** ")

    else:
        print('Please create a strong password with the above guidelines and try again.')
        return


def username_exists_caregiver(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Caregivers WHERE Username = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_username, username)
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['Username'] is not None
    except pymssql.Error as e:
        print("Error occurred when checking username")
        print("Db-Error:", e)
        return
    except Exception as e:
        print("Error:", e)
    finally:
        cm.close_connection()
    return False


def login_patient(tokens):
    # login_patient <username> <password>
    # check 1: if someone's already logged-in, they need to log out first
    global current_patient
    if current_caregiver is not None or current_patient is not None:
        print("Already logged-in! Please use the logout command if a different user wants to login.")
        return

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again! This command requires 2 arguments <username>, <password>, in addition to login_patient function name.")
        return

    username = tokens[1]
    password = tokens[2]

    patient = None
    try:
        patient = Patient(username, password=password).get()
    except pymssql.Error as e:
        print("Login patient failed")
        print("Db-Error:", e)
        return
    except Exception as e:
        print("Error occurred when logging in. Please try again!")
        print("Error:", e)
        return

    # check if the login was successful
    if patient is None:
        print("Error occurred when logging in. Please try again!")
    else:
        print("Patient logged in as: " + username)
        current_patient = patient


def login_caregiver(tokens):
    # login_caregiver <username> <password>
    # check 1: if someone's already logged-in, they need to log out first
    global current_caregiver
    if current_caregiver is not None or current_patient is not None:
        print("Already logged-in! Please use the logout command if a different user wants to login.")
        return

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again! This command requires 2 arguments <username>, <password>, in addition to login_caregiver function name.")
        return

    username = tokens[1]
    password = tokens[2]

    caregiver = None
    try:
        caregiver = Caregiver(username, password=password).get()
    except pymssql.Error as e:
        print("Login caregiver failed")
        print("Db-Error:", e)
        return
    except Exception as e:
        print("Error occurred when logging in. Please try again!")
        print("Error:", e)
        return

    # check if the login was successful
    if caregiver is None:
        print("Error occurred when logging in. Please try again!")
    else:
        print("Caregiver logged in as: " + username)
        current_caregiver = caregiver


def search_caregiver_schedule(tokens):
    # search_caregiver_schedule <date>
    # check 1: if no one is logged in, display a message to login first.
    global current_caregiver
    global current_patient

    if current_caregiver is None and current_patient is None:
        print("Please login as a patient or caregiver to gain access.")
        return

    if len(tokens) != 2:
        print("Please try again! This command requires 1 argument <date> in addition to search_caregiver_schedule function name.")
        return

    date = tokens[1]
    # assume input is hyphenated in the format mm-dd-yyyy
    date_tokens = date.split("-")
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])

    cm = ConnectionManager()
    conn = cm.create_connection()
    search_caregiver = "SELECT Username FROM Availabilities WHERE Time = %s"
    search_vaccine = "SELECT * FROM Vaccines"
    try:
        #d = datetime.datetime(year, month, day)
        #current_caregiver.upload_availability(d)
        cursor = conn.cursor(as_dict=True)
        cursor.execute(search_caregiver, date)

        caregivers = []
        for row in cursor:
            caregivers.append(row['Username'])
        #if caregivers:
            #caregiver_assigned = np.random.choice(caregivers)
            #print(caregiver_assigned)

        cursor.close()

        cursor = conn.cursor(as_dict=True)
        cursor.execute(search_vaccine)

        vaccines = cursor.fetchall()
        if caregivers and vaccines:
            for caregiver in caregivers:
                print("Caregiver(s):", caregiver)
            for vaccine in vaccines:
                print("Vaccines available:", vaccine)
        #elif vaccines == []:
            #print("We do not have sufficient vaccines. The shu is on the way!")
        else:
            print('There are no slots for this day.')

    except pymssql.Error as e:
        print("Caregiver Search Failed")
        print("Db-Error:", e)
        return
    except ValueError:
        print("Please enter a valid date in mm-dd-yyyy format!")
        return
    except Exception as e:
        print("Error occurred while procuring availability")
        print("Error:", e)
        return


def reserve(tokens):
    # reserve <date> <vaccine>
    global current_patient
    if current_patient is None:
        print("Please login as a patient first!")
        return

    if len(tokens) != 3:
        print("Please try again! This command requires 2 arguments <date>, <vaccine>, in addition to reserve function name.")
        return

    date = tokens[1]
    vaccine__name = tokens[2]
    vaccines = ["pfizer", "moderna", "johnson&johnson"]
    if vaccine__name.lower() in vaccines:
    # assume input is hyphenated in the format mm-dd-yyyy
        date_tokens = date.split("-")
        month = int(date_tokens[0])
        day = int(date_tokens[1])
        year = int(date_tokens[2])
        d = datetime.datetime(year, month, day)

        cm = ConnectionManager()
        conn = cm.create_connection()
        search_caregiver = "SELECT Username FROM Availabilities WHERE Time = %s"

        try:
            # Assign random caregiver
            cursor = conn.cursor(as_dict=True)
            cursor.execute(search_caregiver, date)
            caregivers = []
            for row in cursor:
                caregivers.append(row['Username'])
            if caregivers:
                caregiver_assigned = random.choice(caregivers)
            else:
                print("No available appointments for this day. Please try another day.")
                return
            cursor.close()

            # DELETE FROM Availabilties Table WHERE date and time are same as current appointment
            availability_obj = Availability(date, caregiver_assigned)
            availability_obj.delete_availability()

            # INSERT INTO Appointments values ()
            appointment_obj = Appointment(caregiver_assigned, current_patient.get_username(), d, vaccine__name)
            appointment_obj.save_to_db()

            # UPDATE Vaccines SET Doses -= 1 WHERE name = vaccine input %s
            vaccine_obj = Vaccine(vaccine__name, 0)
            vaccine_obj.get()
            vaccine_obj.decrease_available_doses(1)

            if caregivers and vaccine_obj.get_available_doses() > 0:
                print("You have successfully made an appointment with " + str(caregiver_assigned)
                + " and appointment ID: " + str(appointment_obj.get_appointmentID()))
            else:
                print('There are no slots for this day.')

        except pymssql.Error as e:
            print("Error occurred when reserving appointment.")
            print("Db-Error:", e)
            return
        except ValueError:
            print("Please enter a valid date in mm-dd-yyyy format!")
            return
        except Exception as e:
            print("Error:", e)
        finally:
            cm.close_connection()
        return False

    else:
        print("Invalid vaccine name. Please enter one of the three: Pfizer, Moderna or Johnson&Johnson")
        return


def show_appointments(tokens):
    # No arguments, only user login state.

    global current_caregiver
    global current_patient

    if current_caregiver is None and current_patient is None:
        print("Please login as a patient or caregiver to gain access.")
        return

    # Patient logs in.
    if current_patient is not None:
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()
        try:
            appointment_pt = "SELECT AppointmentID, Vaccinename, Time, Caregivername FROM Appointments WHERE Patientname = %s"
            cursor = conn.cursor(as_dict=True)
            cursor.execute(appointment_pt, current_patient.get_username())
            for row in cursor:
                if row:
                    print("Please find your appointment details as follows:")
                    print(row)
                else:
                    print("You have no appointments.")
            cursor.close()
        except pymssql.Error as e:
            print("Error occurred when fetching current caregiver")
            raise e


    # Caregiver logs in.
    if current_caregiver is not None:
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()
        try:
            appointment_cg = "SELECT AppointmentID, Vaccinename, Time, Patientname FROM Appointments WHERE Caregivername = %s"
            cursor = conn.cursor(as_dict=True)
            cursor.execute(appointment_cg, current_caregiver.get_username())
            for row in cursor:
                if row:
                    print("Please find your appointment details as follows:")
                    print(row)
                else:
                    print("You have no appointments.")
            cursor.close()
        except pymssql.Error as e:
            print("Error occurred when fetching current caregiver")
            raise e


def logout(tokens):
    # requires no arguments
    global current_patient
    global current_caregiver
    if current_caregiver is not None:
        print("You have been successfully logged out of caregiver:", current_caregiver.get_username())
        current_caregiver = None
    if current_patient is not None:
        print("You have been successfully logged out of patient:", current_patient.get_username())
        current_patient = None



def upload_availability(tokens):
    #  upload_availability <date>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    # check 2: the length for tokens need to be exactly 2 to include all information (with the operation name)
    if len(tokens) != 2:
        print("Please try again!")
        return

    date = tokens[1]
    # assume input is hyphenated in the format mm-dd-yyyy
    date_tokens = date.split("-")
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])
    try:
        d = datetime.datetime(year, month, day)
        current_caregiver.upload_availability(d)
    except pymssql.Error as e:
        print("Upload Availability Failed")
        print("Db-Error:", e)
        return
    except ValueError:
        print("Please enter a valid date in mm-dd-yyyy format.")
        return
    except Exception as e:
        print("Error occurred when uploading availability")
        print("Error:", e)
        return
    print("Availability uploaded!")


def cancel(tokens):
    if len(tokens) != 2:
        print("Please try again! This command requires 1 argument <Appointment ID> in addition to cancel function name.")
        return

    appointment_ID = tokens[1]
    # remove row from appointments
    # increment vaccine number
    # add to avaialabilities

def add_doses(tokens):
    #  add_doses <vaccine> <number>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    #  check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again!")
        return

    vaccine_name = tokens[1]
    doses = int(tokens[2])
    vaccines = ["pfizer", "moderna", "johnson&johnson"]
    if vaccine_name.lower() in vaccines:
        vaccine = None
        try:
            vaccine = Vaccine(vaccine_name, doses).get()
        except pymssql.Error as e:
            print("Failed to add Vaccine doses to the database.")
            print("Db-Error:", e)
            return
        except Exception as e:
            print("Failed to get Vaccine information")
            print("Error:", e)
            return
    else:
        print("Invalid vaccine name. Please enter one of the three: Pfizer, Moderna or Johnson&Johnson")
        return

    # if the vaccine is not found in the database, add a new (vaccine, doses) entry.
    # else, update the existing entry by adding the new doses
    if vaccine is None:
        vaccine = Vaccine(vaccine_name, doses)
        try:
            vaccine.save_to_db()
        except pymssql.Error as e:
            print("Failed to add new Vaccine to database")
            print("Db-Error:", e)
            return
        except Exception as e:
            print("Failed to add new Vaccine to database")
            print("Error:", e)
            return
    else:
        # if the vaccine is not null, meaning that the vaccine already exists in our table
        try:
            vaccine.increase_available_doses(doses)
        except pymssql.Error as e:
            print("Failed to increase available doses for Vaccine")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Failed to increase available doses for Vaccine")
            print("Error:", e)
            return
    print("Doses updated!")



def start():
    stop = False
    while not stop:
        print()
        print(" *** Please enter one of the following commands *** ")
        print("> create_patient <username> <password>")
        print("> create_caregiver <username> <password>")
        print("> login_patient <username> <password>")
        print("> login_caregiver <username> <password>")
        print("> search_caregiver_schedule <date>")
        print("> reserve <date> <vaccine>")
        print("> upload_availability <date>")
        print("> cancel <appointment_id>")
        print("> add_doses <vaccine> <number>")
        print("> show_appointments")
        print("> logout")
        print("> Quit")
        print()
        response = ""
        print("> Enter: ", end='')

        try:
            response = str(input())
        except ValueError:
            print("Type in a valid argument")
            break

        response = response.lower()
        tokens = response.split(" ")
        if len(tokens) == 0:
            ValueError("Try Again")
            continue
        operation = tokens[0]
        if operation == "create_patient":
            create_patient(tokens)
        elif operation == "create_caregiver":
            create_caregiver(tokens)
        elif operation == "login_patient":
            login_patient(tokens)
        elif operation == "login_caregiver":
            login_caregiver(tokens)
        elif operation == "search_caregiver_schedule":
            search_caregiver_schedule(tokens)
        elif operation == "reserve":
            reserve(tokens)
        elif operation == "upload_availability":
            upload_availability(tokens)
        elif operation == cancel:
            cancel(tokens)
        elif operation == "add_doses":
            add_doses(tokens)
        elif operation == "show_appointments":
            show_appointments(tokens)
        elif operation == "logout":
            logout(tokens)
        elif operation == "quit":
            print("Thank you for using the scheduler, Goodbye!")
            stop = True
        else:
            print("Invalid Argument, please use the commands from the list below (make sure to enter date in mm-dd-yyyy format!):")


if __name__ == "__main__":
    # start command line
    print()
    print("Welcome to the COVID-19 Vaccine Reservation Scheduling Application!")

    start()