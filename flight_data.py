import mysql.connector
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

# Connect to MySQL
airline_conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Priti@02',
    database='airline_system'
)
airline_cursor = airline_conn.cursor()

# ======================
# 1. CREATE TABLES
# ======================

# Airplanes
airline_cursor.execute('''
CREATE TABLE IF NOT EXISTS airplanes (
    airplane_id INT AUTO_INCREMENT PRIMARY KEY,
    model VARCHAR(50) NOT NULL,
    manufacturer VARCHAR(100) NOT NULL,
    capacity INT NOT NULL
) ENGINE=InnoDB
''')

airline_cursor.execute('''
CREATE TABLE IF NOT EXISTS airplane_status (
    status_id INT AUTO_INCREMENT PRIMARY KEY,
    airplane_id INT NOT NULL,
    status VARCHAR(50) NOT NULL,
    updated_on DATE,
    engineer_name VARCHAR(100) NOT NULL,
    maintenance_date DATE,
    remarks TEXT,
    FOREIGN KEY (airplane_id) REFERENCES airline_system.airplanes(airplane_id)
) ENGINE=InnoDB
''')
airline_conn.commit()

# Connect to MySQL
flights_conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Priti@02',
    database='flights_system'
)
flights_cursor = flights_conn.cursor()

# Flights
flights_cursor.execute('''
CREATE TABLE IF NOT EXISTS flights (
    flight_id INT AUTO_INCREMENT PRIMARY KEY,
    airplane_id INT NOT NULL,
    flight_number VARCHAR(20) NOT NULL,
    origin VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    FOREIGN KEY (airplane_id) REFERENCES airline_system.airplanes(airplane_id)
) ENGINE=InnoDB
''')

flights_cursor.execute('''
CREATE TABLE IF NOT EXISTS flight_status (
    status_id INT AUTO_INCREMENT PRIMARY KEY,
    flight_id INT NOT NULL,
    takeoff_time DATETIME,
    takeoff_place VARCHAR(100) NOT NULL,
    landing_time DATETIME,
    landing_place VARCHAR(100) NOT NULL,
    delay_minutes INT ,
    status VARCHAR(50) NOT NULL,
    FOREIGN KEY (flight_id) REFERENCES flights_system.flights(flight_id)
) ENGINE=InnoDB
''')
flights_conn.commit()

# Connect to MySQL
passenger_conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Priti@02',
    database='passenger_system'
)
passenger_cursor = passenger_conn.cursor()


passenger_cursor.execute('''
CREATE TABLE IF NOT EXISTS passengers (
    passenger_id INT AUTO_INCREMENT PRIMARY KEY,
    lastname VARCHAR(50) NOT NULL,
    firstname VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    age INT,
    dob DATE,
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    gender ENUM('Male', 'Female'),
    phone VARCHAR(20) NOT NULL UNIQUE
) ENGINE=InnoDB
''')

passenger_cursor.execute('''
CREATE TABLE IF NOT EXISTS flight_passengers (
    passenger_flight_id INT AUTO_INCREMENT PRIMARY KEY,
    flight_id INT,
    passenger_id INT,
    seat_number VARCHAR(10),
    FOREIGN KEY (flight_id) REFERENCES flights_system.flights(flight_id),
    FOREIGN KEY (passenger_id) REFERENCES passenger_system.passengers(passenger_id)
) ENGINE=InnoDB
''')

passenger_cursor.execute('''
CREATE TABLE IF NOT EXISTS connecting_flights (
    connection_id INT AUTO_INCREMENT PRIMARY KEY,
    passenger_id INT,
    main_flight_id INT,
    connecting_flight_id INT,
    connection_notes TEXT,
    FOREIGN KEY (passenger_id) REFERENCES passenger_system.passengers(passenger_id),
    FOREIGN KEY (main_flight_id) REFERENCES flights_system.flights(flight_id),
    FOREIGN KEY (connecting_flight_id) REFERENCES flights_system.flights(flight_id)                     
) ENGINE=InnoDB
''')
passenger_conn.commit()

# =======================
# 2. INSERT FAKE DATA
# =======================

airplane_ids = []
for _ in range(50):
    """
    adds data about airplanes
    """
    model = fake.bothify("Model-###")
    manufacturer = fake.company()
    capacity = random.randint(100, 300)
    

    airline_cursor.execute('''
        INSERT INTO airplanes (model, manufacturer, capacity)
        VALUES (%s, %s, %s)
    ''', (model, manufacturer, capacity))

    active_status_sentence = [
    "The aircraft is currently active and ready for scheduled flights.",
    "This airplane is in active service and operating on domestic routes.",
    "The jet is fully operational and assigned to regular flight duties.",
    "The aircraft is part of the current active fleet.",
    "It is actively serving international routes without interruptions."]

    maintenance_status_sentences = [
    "The aircraft is undergoing routine maintenance checks.",
    "This airplane is temporarily out of service for scheduled maintenance.",
    "The plane is in the hangar for a thorough systems inspection.",
    "It is currently grounded for engine diagnostics and repairs.",
    "The aircraft is under maintenance and unavailable for flight operations."]

    retired_status_sentences = [
        "The aircraft has been officially retired from the fleet.",
        "This plane was decommissioned after 25 years of service.",
        "The retired aircraft is now displayed in the aviation museum.",
        "It is no longer in active service and has been removed from flight logs.",
        "The airplane has been retired and stored at the desert facility."
    ]

    airplane_id = airline_cursor.lastrowid
    airplane_ids.append(airplane_id)

    status = random.choice(['active', 'maintenance', 'retired'])
    if status =='active':
        remark = random.choice(active_status_sentence)
    elif status == 'maintenance':
        remark = random.choice(maintenance_status_sentences)
    else:
        remark = random.choice(retired_status_sentences)

    # Status
    airline_cursor.execute('''
        INSERT INTO airplane_status (airplane_id, status, updated_on, engineer_name,maintenance_date, remarks)
        VALUES (%s, %s, %s,%s, %s, %s)
    ''', (airplane_id, status, fake.date_this_year(), fake.name(), fake.date_between('-2y', 'today'), remark))
airline_conn.commit()
airline_conn.close()

# Flights
flight_ids = []
for _ in range(200):
    airplane_id = random.choice(airplane_ids)
    flight_number = fake.bothify("FL###")
    origin = fake.city()
    destination = fake.city()
    while destination == origin:
        destination = fake.city()

    flights_cursor.execute('''
        INSERT INTO flights (airplane_id, flight_number, origin, destination)
        VALUES (%s, %s, %s, %s)
    ''', (airplane_id, flight_number, origin, destination))

    flight_id = flights_cursor.lastrowid
    flight_ids.append(flight_id)

    takeoff_time = fake.date_time_between(start_date='-3d', end_date='+2d')
    landing_time = takeoff_time + timedelta(hours=random.randint(1, 5))

    flights_cursor.execute('''
        INSERT INTO flight_status (flight_id, takeoff_time, takeoff_place, landing_time, landing_place, delay_minutes, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (
        flight_id,
        takeoff_time,
        origin,
        landing_time,
        destination,
        random.choice([0, 15, 30, 60]),
        random.choice(['scheduled', 'delayed', 'departed', 'landed', 'cancelled'])
    ))
flights_conn.commit()
flights_conn.close()


# Passengers
passenger_ids = []
emails = set()
for _ in range(2000):
    firstname = fake.first_name()
    lastname = fake.last_name()
    email = fake.email()
    counter = 1
    while email in emails:
        email = fake.email().split('@')[0] + str(counter) + '@' + fake.email().split('@')[1]
        counter += 1
    
    emails.add(email)
    
    dob = fake.date_of_birth(minimum_age=10, maximum_age=85)
    age = datetime.now().year - dob.year
    address = fake.street_address()
    city = fake.city()
    state = fake.state()
    country = fake.country()
    gender = random.choice(['Male', 'Female'])
    phone = fake.phone_number()

    if len(phone) > 20:
        phone = phone[:20]

    passenger_cursor.execute('''
        INSERT INTO passengers (lastname, firstname, email, age, dob, address, city, state, country, gender, phone)
        VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (lastname, firstname, email, age, dob, address, city, state, country, gender, phone))

    passenger_id = passenger_cursor.lastrowid
    passenger_ids.append(passenger_id)

    # Assign 1 or 2 flights
    assigned_flights = random.sample(flight_ids, k=random.randint(1, 2))
    for flight_id in assigned_flights:
        seat = f"{random.randint(1, 30)}{random.choice(['A', 'B', 'C', 'D'])}"
        passenger_cursor.execute('''
            INSERT INTO flight_passengers (flight_id, passenger_id, seat_number)
            VALUES (%s, %s, %s)
        ''', (flight_id, passenger_id, seat))

    if len(assigned_flights) > 1:
        passenger_cursor.execute('''
            INSERT INTO connecting_flights (passenger_id, main_flight_id, connecting_flight_id, connection_notes)
            VALUES (%s, %s, %s, %s)
        ''', (
            passenger_id,
            assigned_flights[0],
            assigned_flights[1],
            "Layover at connecting airport"
        ))



passenger_conn.commit()
passenger_conn.close()
print("MySQL airline database populated successfully.")