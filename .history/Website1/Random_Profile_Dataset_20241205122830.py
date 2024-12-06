import json
import random
import string
from datetime import datetime, timedelta

ActivationDate = None
DeactivationDate = None
EmployeeStatus = None
EmployeeType = None
BadgeStatus = None
Region = None
BuildingLocation= None
ActiveBadge = False
LocationInOrOut = None
GeneralAccess = False

# Sample lists of values for different fields
first_names = ['James',
'Michael',
'Robert',
'John',
'David',
'William',
'Richard',
'Joseph',
'Thomas',
'Christopher',
'Charles',
'Daniel',
'Matthew',
'Anthony',
'Mark',
'Donald',
'Steven',
'Andrew',
'Paul',
'Joshua',
'Kenneth',
'Kevin',
'Brian',
'Timothy',
'Ronald',
'George',
'Jason',
'Edward',
'Jeffrey',
'Ryan',
'Jacob',
'Nicholas',
'Gary',
'Eric',
'Jonathan',
'Stephen',
'Larry',
'Justin',
'Scott',
'Brandon',
'Benjamin',
'Samuel',
'Gregory',
'Alexander',
'Patrick',
'Frank',
'Raymond',
'Jack',
'Dennis',
'Jerry',
'Tyler',
'Aaron',
'Jose',
'Adam',
'Nathan',
'Henry',
'Zachary',
'Douglas',
'Peter',
'Kyle',
'Noah',
'Ethan',
'Jeremy',
'Christian',
'Walter',
'Keith',
'Austin',
'Roger',
'Terry',
'Sean',
'Gerald',
'Carl',
'Dylan',
'Harold',
'Jordan',
'Jesse',
'Bryan',
'Lawrence',
'Arthur',
'Gabriel',
'Bruce',
'Logan',
'Billy',
'Joe',
'Alan',
'Juan',
'Elijah',
'Willie',
'Albert',
'Wayne',
'Randy',
'Mason',
'Vincent',
'Liam',
'Roy',
'Bobby',
'Caleb',
'Bradley',
'Russell',
'Lucas',
'Mary',
'Patricia',
'Jennifer',
'Linda',
'Elizabeth',
'Barbara',
'Susan',
'Jessica',
'Karen',
'Sarah',
'Lisa',
'Nancy',
'Sandra',
'Betty',
'Ashley',
'Emily',
'Kimberly',
'Margaret',
'Donna',
'Michelle',
'Carol',
'Amanda',
'Melissa',
'Deborah',
'Stephanie',
'Rebecca',
'Sharon',
'Laura',
'Cynthia',
'Dorothy',
'Amy',
'Kathleen',
'Angela',
'Shirley',
'Emma',
'Brenda',
'Pamela',
'Nicole',
'Anna',
'Samantha',
'Katherine',
'Christine',
'Debra',
'Rachel',
'Carolyn',
'Janet',
'Maria',
'Olivia',
'Heather',
'Helen',
'Catherine',
'Diane',
'Julie',
'Victoria',
'Joyce',
'Lauren',
'Kelly',
'Christina',
'Ruth',
'Joan',
'Virginia',
'Judith',
'Evelyn',
'Hannah',
'Andrea',
'Megan',
'Cheryl',
'Jacqueline',
'Madison',
'Teresa',
'Abigail',
'Sophia',
'Martha',
'Sara',
'Gloria',
'Janice',
'Kathryn',
'Ann',
'Isabella',
'Judy',
'Charlotte',
'Julia',
'Grace',
'Amber',
'Alice',
'Jean',
'Denise',
'Frances',
'Danielle',
'Marilyn',
'Natalie',
'Beverly',
'Diana',
'Brittany',
'Theresa',
'Kayla',
'Alexis',
'Doris',
'Lori',
'Tiffany'
]
last_names = ['Smith',
'Johnson',
'Williams',
'Brown',
'Jones',
'Garcia',
'Miller',
'Davis',
'Rodriguez',
'Martinez',
'Hernandez',
'Lopez',
'Gonzalez',
'Wilson',
'Anderson',
'Thomas',
'Taylor',
'Moore',
'Jackson',
'Martin',
'Lee',
'Perez',
'Thompson',
'White',
'Harris',
'Sanchez',
'Clark',
'Ramirez',
'Lewis',
'Robinson',
'Walker',
'Young',
'Allen',
'King',
'Wright',
'Scott',
'Torres',
'Nguyen',
'Hill',
'Flores',
'Green',
'Adams',
'Nelson',
'Baker',
'Hall',
'Rivera',
'Campbell',
'Mitchell',
'Carter',
'Roberts',
'Gomez',
'Phillips',
'Evans',
'Turner',
'Diaz',
'Parker',
'Cruz',
'Edwards',
'Collins',
'Reyes',
'Stewart',
'Morris',
'Morales',
'Murphy',
'Cook',
'Rogers',
'Gutierrez',
'Ortiz',
'Morgan',
'Cooper',
'Peterson',
'Bailey',
'Reed',
'Kelly',
'Howard',
'Ramos',
'Kim',
'Cox',
'Ward',
'Richardson',
'Watson',
'Brooks',
'Chavez',
'Wood',
'James',
'Bennett',
'Gray',
'Mendoza',
'Ruiz',
'Hughes',
'Price',
'Alvarez',
'Castillo',
'Sanders',
'Patel',
'Myers',
'Long',
'Ross',
'Foster',
'Jimenez',
'Powell',
'Jenkins',
'Perry',
'Russell',
'Sullivan',
'Bell',
'Coleman',
'Butler',
'Henderson',
'Barnes',
'Gonzales',
'Fisher',
'Vasquez',
'Simmons',
'Romero',
'Jordan',
'Patterson',
'Alexander',
'Hamilton',
'Graham',
'Reynolds',
'Griffin',
'Wallace',
'Moreno',
'West',
'Cole',
'Hayes',
'Bryant',
'Herrera',
'Gibson',
'Ellis',
'Tran',
'Medina',
'Aguilar',
'Stevens',
'Murray',
'Ford',
'Castro',
'Marshall',
'Owens',
'Harrison',
'Fernandez',
'Mcdonald',
'Woods',
'Washington',
'Kennedy',
'Wells',
'Vargas',
'Henry',
'Chen',
'Freeman',
'Webb',
'Tucker',
'Guzman',
'Burns',
'Crawford',
'Olson',
'Simpson',
'Porter',
'Hunter',
'Gordon',
'Mendez',
'Silva',
'Shaw',
'Snyder',
'Mason',
'Dixon',
'Muñoz',
'Hunt',
'Hicks',
'Holmes',
'Palmer',
'Wagner',
'Black',
'Robertson',
'Boyd',
'Rose',
'Stone',
'Salazar',
'Fox',
'Warren',
'Mills',
'Meyer',
'Rice',
'Schmidt',
'Garza',
'Daniels',
'Ferguson',
'Nichols',
'Stephens',
'Soto',
'Weaver',
'Ryan',
'Gardner',
'Payne',
'Grant',
'Dunn',
'Kelley',
'Spencer',
'Hawkins'
]
employee_types = ["Employee", "Employee (Seasonal)", "Contractor"]
employee_statuses = ["Active", "Terminated", "Suspended"]
regions = ["AMER", "EMEA", "APAC"]
buildings_countries = ["KAFW/USA"]
#buildings_countries = ["LUX12/LUX", "KAFW/USA", "KCVG/USA", "ABE2/USA", "DBW8/DEU", "BLR96/IND"]
manager_login = ["jgfkwo", "oslfow", "tmdowq", "plmiaa", "reeiop", "qmjjui"]

badge_status = ["Active", "Lost", "Returned", "Terminated", "Broken", "Use/Lose (System)", "Suspended", "Expired (System)"]
badge_type = ["Air Employee Seasonal (pic)", "Air Employee (pic)", "Employee (pic)", "Employee Seasonal (pic)", "Employee 5yr (pic)", "Air Employee 5yr (pic)", "Contractor (pic)", "Air Contractor(pic)"]

accesslvl = ["DFW7-1-GENERAL ACCESS", "DFW7-2-TRAILER YARD ACCESS", "KAFW-1-GENERAL ACCESS", "KAFW-2-TRAILER YARD ACCESS",
             "LUX12-1-GENERAL ACCESS", "LUX12-2-TRAILER YARD ACCESS", "KCVG-1-GENERAL ACCESS", "KCVG-2-TRAILER YARD ACCESS",
             "ABE2-1-GENERAL ACCESS", "ABE2-2-TRAILER YARD ACCESS", "DBW8-1-GENERAL ACCESS", "DBW8-2-TRAILER YARD ACCESS",
             "BLR96-1-GENERAL ACCESS", "BLR96-2-TRAILER YARD ACCESS", "KRFD-1-GENERAL ACCESS", "KRFD-2-TRAILER YARD ACCESS"]

# Function to generate a random string (for IDs, Logins, etc.)
def generate_random_string(length=32, Just_Numbers=False, Just_Letters=False):
    if Just_Numbers:
        # Use only digits
        return ''.join(random.choices(string.digits, k=length))
    elif Just_Letters:
        # Use only letters (lowercase and uppercase)
        return ''.join(random.choices((string.ascii_letters).lower(), k=length))
    else:
        # Use both letters and numbers
        return ''.join(random.choices((string.ascii_letters).lower() + string.digits, k=length))

def generate_random_badgeStatus():
    global BadgeStatus, ActiveBadge

    if ActiveBadge:
        exclude_indices = [0, 5, 6, 7]
        BadgeStatus = random.choice([status for i, status in enumerate(badge_status) if i not in exclude_indices])
        return BadgeStatus

    if EmployeeStatus == "Active":
        BadgeStatus = random.choice(badge_status)
    elif EmployeeStatus == "Terminated":
        exclude_indices = [0, 1, 4, 5, 6, 7]
        BadgeStatus = random.choice([status for i, status in enumerate(badge_status) if i not in exclude_indices])
    else:
        exclude_indices = [0]
        BadgeStatus = random.choice([status for i, status in enumerate(badge_status) if i not in exclude_indices])

    if BadgeStatus == "Active" or "Use/Lose (System)" or "Suspended":
        ActiveBadge = True        

    return BadgeStatus

def generate_random_badgeType(Tenure):
    if EmployeeType == "Contractor":
        exclude_indices = [0, 1, 2, 3, 4, 5]
        BadgeType = random.choice([status for i, status in enumerate(badge_type) if i not in exclude_indices])
    elif EmployeeType == "Employee (Seasonal)":
        exclude_indices = [1, 2, 4, 5 , 6, 7]
        BadgeType = random.choice([status for i, status in enumerate(badge_type) if i not in exclude_indices])
    else:
        if Tenure >= "5 years":
            exclude_indices = [0, 1, 2, 3, 6, 7]
            BadgeType = random.choice([status for i, status in enumerate(badge_type) if i not in exclude_indices])
        else:
            exclude_indices = [0, 3, 4, 5, 6, 7]
            BadgeType = random.choice([status for i, status in enumerate(badge_type) if i not in exclude_indices])
    
    return BadgeType

def generate_random_employeeStatus():
    global EmployeeStatus
    EmployeeStatus = random.choice(employee_statuses)
    return EmployeeStatus

def generate_random_employeeType():
    global EmployeeType
    EmployeeType = random.choice(employee_types)
    return EmployeeType

def generate_random_Date(BadgeActivation=False, BadgeDeactivation=False, LastUpdate=False):
    global ActivationDate, DeactivationDate
    def random_time():
        """Generate a random time in HH:MM:SS format."""
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        return f"{hour:02}:{minute:02}:{second:02}"  # Zero-padded time

    if BadgeActivation:
        # Base date configuration
        BASE_DATE = datetime(2024, 12, 5)
        
        # Define the year range
        year = random.randint(2019, 2024)
        
        # Generate a random month and day
        month = random.randint(1, 12)
        day = random.randint(1, 28)  # Use 28 to avoid invalid days in months like February
        
        # Generate the date
        random_date = datetime(year, month, day)
        
        # Ensure it's not past the base date
        if random_date > BASE_DATE:
            random_date = BASE_DATE - timedelta(days=random.randint(1, 365))  # Adjust back
        
        # Generate a random activation date within the last 5 years
        ActivationDate = BASE_DATE - timedelta(days=random.randint(0, 1825))
        return ActivationDate.strftime("%Y-%m-%d") + " " + random_time()

    elif BadgeDeactivation:
        DeactivationDate = ActivationDate + timedelta(days=730)
        DeactivationDate = DeactivationDate.replace(hour=23, minute=59, second=59)
        return DeactivationDate.strftime("%Y-%m-%d %H:%M:%S")

    elif LastUpdate:
        LastUpdateDate = ActivationDate + timedelta(days=random.randint(1, 729))
        return LastUpdateDate.strftime("%Y-%m-%d") + " " + random_time()

def generate_random_Region():
    global Region
    Region = random.choice(regions)
    return Region

def generate_random_Building():
    global BuildingLocation

    if Region == "AMER":
        exclude_indices = [0, 4, 5]
        BuildingLocation = random.choice([status for i, status in enumerate(buildings_countries) if i not in exclude_indices])
    elif Region == "EMEA":
        exclude_indices = [1, 2, 3, 5]
        BuildingLocation = random.choice([status for i, status in enumerate(buildings_countries) if i not in exclude_indices])
    else:
        BuildingLocation = "BLR96/IND"

    return BuildingLocation

def generate_random_LastLocationRead():
    global LocationInOrOut, BadgeStatus
    if LocationInOrOut == "In":
        Location = f"{(BuildingLocation.split('/')[0])} Out"
    else:
        if BadgeStatus == "Active":
            LocationInOrOut = random.choice(["In", "Out", "In"])
            Location = f"{(BuildingLocation.split('/')[0])} {LocationInOrOut}"
        else:
            Location = f"{(BuildingLocation.split('/')[0])} Out"

    return Location

def generate_random_AccessLvl():
    global LocationInOrOut, GeneralAccess, BuildingLocation
    print(LocationInOrOut, GeneralAccess, BuildingLocation)
    if LocationInOrOut == "In":
        if GeneralAccess:
            AccessLvl = f"{BuildingLocation.split('/')[0]}-1-GENERAL ACCESS"
            while AccessLvl == f"{BuildingLocation.split('/')[0]}-1-GENERAL ACCESS":
                AccessLvl = random.choice(accesslvl)
            return AccessLvl
        else:
            AccessLvl = f"{BuildingLocation.split('/')[0]}-1-GENERAL ACCESS"
            GeneralAccess = True
            return AccessLvl
    else:
        AccessLvl = random.choice(accesslvl)
        return AccessLvl

# Generate random profile
def generate_profile():
    global Region, BuildingLocation, ActiveBadge, LocationInOrOut
    badge_count = random.randint(0, 5)  # Generate a random number of badges
    badges = []

    accessLvl_count = random.randint(0, 5)  # Generate a random number of badges
    accessLvl = []

    Login = generate_random_string(Just_Letters=True, length=6)
    Employee_ID = generate_random_string(Just_Numbers=True, length=9)
    Person_ID = generate_random_string()
    Barcode = generate_random_string(Just_Numbers=True, length=8)
    First_Name = random.choice(first_names)
    Last_Name = random.choice(last_names)
    Employee_Type = generate_random_employeeType()
    Employee_Status = generate_random_employeeStatus()
    Manager = random.choice(manager_login)
    Tenure = str(random.randint(1, 9)) + " years, " + str(random.randint(1, 12)) + " months, " + str(random.randint(1, 28)) + " days"
    Region = generate_random_Region()
    BuildingLocation = generate_random_Building()

    for _ in range(badge_count):
        badges.append({
            "Badge_ID": generate_random_string(Just_Numbers=True, length=8),
            "Badge_Status": generate_random_badgeStatus(),
            "Badge_Type": generate_random_badgeType(Tenure),
            "Badge_ActivateOn": generate_random_Date(BadgeActivation=True),
            "Badge_DeactivateOn": generate_random_Date(BadgeDeactivation=True),
            "Badge_LastUpdatedUTC": generate_random_Date(LastUpdate=True),
            "Badge_LastLocationReaderName": generate_random_LastLocationRead(),
            "Badge_LastLocationEventType": "Access Granted",
        })
        #if BadgeStatus == "Use/Lose (System)" or "Suspended":
        #    accessLvl_count = 0

    if badge_count == 0:
        accessLvl_count = 0
    #if not ActiveBadge:
    #    accessLvl_count = 0

    ActiveBadge = False

    for _ in range(accessLvl_count):
        accessLvl.append({
            "AccessLevel": generate_random_AccessLvl(),
            "AccessLevel_ActivateOn": random.choice(badge_status),
            "AccessLevel_Deactivate": random.choice(badge_status)
        })

    if accessLvl_count == 0 and LocationInOrOut == "In":
        accessLvl_count = "1"
        LocationInOrOut == "In"
        accessLvl.append({
            "AccessLevel": generate_random_AccessLvl(),
            "AccessLevel_ActivateOn": random.choice(badge_status),
            "AccessLevel_Deactivate": random.choice(badge_status)
        })

    LocationInOrOut = None

    return {
        "Login": Login,
        "Employee_ID": Employee_ID,
        "Person_ID": Person_ID,
        "Barcode": Barcode,
        "First_Name": First_Name,
        "Last_Name": Last_Name,
        "Employee_Type": Employee_Type,
        "Employee_Status": Employee_Status,
        "Manager": Manager,
        "Tenure": Tenure,
        "Region": Region,
        "Building/Country": BuildingLocation,

        # Badge data
        "Badge_Count": badge_count,
        "Badges": badges,

        # Access level data
        "AccessLvl_Count": accessLvl_count,
        "AccessLvl": accessLvl,
        
    }

# Generate 3000 profiles
profiles = [generate_profile() for _ in range(10)]

# Save the profiles to a JSON file
with open('Website1/fake_data.json', 'w') as f:
    json.dump(profiles, f, indent=4)

print("Fake dataset generated and saved to fake_data.json")

