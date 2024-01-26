CREATE TABLE Caregivers (
    Username varchar(255),
    Salt BINARY(16),
    Hash BINARY(16),
    PRIMARY KEY (Username)
);

CREATE TABLE Patients (
    Username varchar(255),
    Salt BINARY(16),
    Hash BINARY(16),
    PRIMARY KEY (Username)
);

CREATE TABLE Availabilities (
    Time date,
    Username varchar(255) REFERENCES Caregivers,
    PRIMARY KEY (Time, Username)
);

CREATE TABLE Vaccines (
    Name varchar(255),
    Doses int,
    PRIMARY KEY (Name)
);

CREATE TABLE Appointments (
    AppointmentID VARCHAR(255),
    Caregivername VARCHAR(255) REFERENCES Caregivers(Username),
    Patientname VARCHAR(255) REFERENCES Patients(Username),
    Time date,
    Vaccinename VARCHAR(255) REFERENCES Vaccines(Name)
    PRIMARY KEY (AppointmentID)
);

-- Time date,
-- Time varchar(10),
