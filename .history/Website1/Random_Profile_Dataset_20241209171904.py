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
ActivationDate_Time = None
LastUpdateDate_Time = None
AccessLevelActivateOn = None
index = 0

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
employee_types = ["Employee", "Employee (Seasonal)", "Contractor", "Employee", "Employee"]
employee_statuses = ["Active", "Terminated", "Suspended", "Active", "Active"]
regions = ["AMER", "EMEA", "APAC"]
buildings_countries = ["LUX12/LUX", "KAFW/USA", "KCVG/USA", "ABE2/USA", "DBW8/DEU", "BLR96/IND"]
manager_login = ["jgfkwo", "oslfow", "tmdowq", "plmiaa", "reeiop", "qmjjui"]

badge_status = ["Active", "Lost", "Returned", "Terminated", "Broken", "Use/Lose (System)", "Suspended", "Expired (System)", "Active", "Active", "Active"]
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
        exclude_indices = [0, 5, 6, 7, 8, 9, 10]
        BadgeStatus = random.choice([status for i, status in enumerate(badge_status) if i not in exclude_indices])
        return BadgeStatus

    if EmployeeStatus == "Active":
        BadgeStatus = random.choice(badge_status)
    elif EmployeeStatus == "Terminated":
        exclude_indices = [0, 1, 4, 5, 6, 7, 8, 9, 10]
        BadgeStatus = random.choice([status for i, status in enumerate(badge_status) if i not in exclude_indices])
    else:
        exclude_indices = [0, 8, 9, 10]
        BadgeStatus = random.choice([status for i, status in enumerate(badge_status) if i not in exclude_indices])

    if BadgeStatus == "Active":
        ActiveBadge = True
    if BadgeStatus == "Use/Lose (System)":
        ActiveBadge = True
    if BadgeStatus == "Suspended":
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

def generate_random_Date(BadgeActivation=False, BadgeDeactivation=False, LastUpdate=False, base_date=None, activation_date=None, next_activation_date=None):
    global ActivationDate, DeactivationDate, ActivationDate_Time, LastUpdateDate_Time
    def random_time():
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        return f"{hour:02}:{minute:02}:{second:02}"  # Zero-padded time

    if BadgeActivation:
        # If no base_date is provided, use the current date
        if base_date is None:
            base_date = datetime(2024, 12, 5)

        # Generate a random activation date up to 5 years before the base date
        days_back = random.randint(0, 1825)
        ActivationDate = base_date - timedelta(days=days_back)
        ActivationDate_Time = ActivationDate.strftime("%Y-%m-%d") + " " + random_time()
        return ActivationDate_Time

    elif BadgeDeactivation:
        # Deactivate date 2 years after activation
        DeactivationDate = ActivationDate + timedelta(days=730)
        DeactivationDate = DeactivationDate.replace(hour=23, minute=59, second=59)
        return DeactivationDate.strftime("%Y-%m-%d %H:%M:%S")

    elif LastUpdate:
        # Ensure activation_date and next_activation_date are datetime objects
        if isinstance(activation_date, str):
            activation_date = datetime.strptime(activation_date, "%Y-%m-%d %H:%M:%S")
        if isinstance(next_activation_date, str):
            next_activation_date = datetime.strptime(next_activation_date, "%Y-%m-%d %H:%M:%S")

        # Default next_activation_date to current time if not provided
        if next_activation_date is None:
            next_activation_date = datetime.now()

        # Generate a LastUpdate date between activation_date and next_activation_date
        delta_days = (next_activation_date - activation_date).days
        if delta_days > 1:
            days_offset = random.randint(1, delta_days - 1)
        else:
            days_offset = 1  # Ensure at least 1 day offset if delta is too small

        LastUpdateDate = activation_date + timedelta(days=days_offset)
        LastUpdateDate_Time = LastUpdateDate.strftime("%Y-%m-%d") + " " + random_time()

        return LastUpdateDate_Time

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
    global LocationInOrOut, BadgeStatus, BuildingLocation
    if BadgeStatus == "Active":
        if LocationInOrOut == "In":
            Location = f"{(BuildingLocation.split('/')[0])} Out"
        else:
            LocationInOrOut = random.choice(["In", "Out", "In"])
            Location = f"{(BuildingLocation.split('/')[0])} {LocationInOrOut}"
    else:
        Location = f"{(BuildingLocation.split('/')[0])} Out"

    return Location

def generate_random_AccessLvl(ListOfLvls):
    global LocationInOrOut, GeneralAccess, BuildingLocation, badge_status
    if LocationInOrOut == "In":
        AccessLvl = f"{BuildingLocation.split('/')[0]}-1-GENERAL ACCESS"
        ListOfLvls.append(AccessLvl)
        LocationInOrOut = None
    else:
        AccessLvl = random.choice(accesslvl)
        while AccessLvl in ListOfLvls:
            AccessLvl = random.choice(accesslvl)
        ListOfLvls.append(AccessLvl)

    return AccessLvl

def generate_random_AccessLevelActivateOn():
    global AccessLevelActivateOn, LastUpdateDate_Time, AccessLevelActivateOn
    choice = random.choice(["BadgeActivation", "LastUpdate", "Permanent"])
    if choice == "BadgeActivation":
        AccessLevelActivateOn = ActivationDate_Time
        return AccessLevelActivateOn
    elif choice == "LastUpdate":
        AccessLevelActivateOn = LastUpdateDate_Time
        return AccessLevelActivateOn
    else:
        AccessLevelActivateOn = "PERMANENT"
        return AccessLevelActivateOn

def generate_random_AccessLevelDeactivateOn():
    global AccessLevelActivateOn, AccessLevelActivateOn
    if AccessLevelActivateOn == "PERMANENT":
        return "PERMANENT"
    else:
        activate_on_datetime = datetime.strptime(AccessLevelActivateOn, "%Y-%m-%d %H:%M:%S")
        deactivate_on_datetime = (activate_on_datetime + timedelta(days=730)).replace(hour=23, minute=59, second=59)
        return deactivate_on_datetime.strftime("%Y-%m-%d %H:%M:%S")

# Generate random profile
def generate_profile():
    global Region, BuildingLocation, ActiveBadge, LocationInOrOut, GeneralAccess, index

    #Generate a random image URL using DiceBear
    random_seed = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=7))
    styles = [
        'adventurer', 'adventurer-neutral', 'avataaars', 'avataaars-neutral',
        'big-ears', 'big-ears-neutral', 'big-smile', 'bottts', 'bottts-neutral'
    ]
    random_style = random.choice(styles)
    profile_image = f"https://api.dicebear.com/6.x/{random_style}/svg?seed={random_seed}"

    badge_count = random.randint(0, 5)  # Generate a random number of badges
    badges = []

    accessLvl_count = random.randint(0, 5)  # Generate a random number of badges
    accessLvl = []

    Employee_ID = generate_random_string(Just_Numbers=True, length=9)
    Person_ID = generate_random_string()
    Barcode = generate_random_string(Just_Numbers=True, length=8)
    First_Name = random.choice(first_names)
    Last_Name = random.choice(last_names)
    Employee_Type = generate_random_employeeType()
    Employee_Status = generate_random_employeeStatus()
    Login = None

    if Employee_Status == "Active":
        if Employee_Type == "Employee":
            if index < len(manager_login):
                Login = manager_login[index]
                index = index + 1
            else:
                Login = generate_random_string(Just_Letters=True, length=6)
        else:
            Login = generate_random_string(Just_Letters=True, length=6)
    else:
        Login = generate_random_string(Just_Letters=True, length=6)

    Manager = random.choice(manager_login)
    while Manager == Login:
        Manager = random.choice(manager_login)
    Tenure = str(random.randint(1, 9)) + " years, " + str(random.randint(1, 11)) + " months, " + str(random.randint(1, 28)) + " days"
    Region = generate_random_Region()
    BuildingLocation = generate_random_Building()

    # Generate random base date for sorting badges
    base_date = datetime(2024, 12, 5)
    latest_allowed_date = base_date

    for i in range(badge_count):
        # Generate badge activation date
        badge_activate = generate_random_Date(BadgeActivation=True, base_date=latest_allowed_date)

        # Generate LastUpdate ensuring it falls after activation but before the latest allowed date
        badge_lastupdate = generate_random_Date(
            LastUpdate=True, 
            activation_date=badge_activate, 
            next_activation_date=latest_allowed_date
        )

        # Generate badge deactivation date
        badge_deactivate = generate_random_Date(BadgeDeactivation=True)

        badges.append({
            "Badge_ID": generate_random_string(Just_Numbers=True, length=8),
            "Badge_Status": generate_random_badgeStatus(),
            "Badge_Type": generate_random_badgeType(Tenure),
            "Badge_ActivateOn": badge_activate,
            "Badge_DeactivateOn": badge_deactivate,
            "Badge_LastUpdatedUTC": badge_lastupdate,
            "Badge_LastLocationReaderName": generate_random_LastLocationRead(),
            "Badge_LastLocationEventType": "Access Granted",
        })

        # Update the latest allowed date for the next badge to ensure proper chronological order
        latest_allowed_date = datetime.strptime(badge_activate, "%Y-%m-%d %H:%M:%S")

        if BadgeStatus == "Use/Lose (System)":
            #print(accessLvl_count, BadgeStatus)
            accessLvl_count = 0
        if BadgeStatus == "Suspended":
            #print(accessLvl_count, BadgeStatus)
            accessLvl_count = 0

    # Sort badges by activation date (newest to oldest)
    badges.sort(key=lambda b: datetime.strptime(b["Badge_ActivateOn"], "%Y-%m-%d %H:%M:%S"), reverse=True)

    if badge_count == 0:
        accessLvl_count = 0
    global ActiveBadge
    if not ActiveBadge:
        accessLvl_count = 0

    ListOfLvls = []

    for _ in range(accessLvl_count):
        RandomAccess = generate_random_AccessLvl(ListOfLvls)
        accessLvl.append({
            "AccessLevel": RandomAccess,
            "AccessLevel_ActivateOn": generate_random_AccessLevelActivateOn(),
            "AccessLevel_Deactivate": generate_random_AccessLevelDeactivateOn()
        })

    if accessLvl_count == 0 and LocationInOrOut == "In":
        accessLvl_count = "1"
        accessLvl.append({
            "AccessLevel": f"{BuildingLocation.split('/')[0]}-1-GENERAL ACCESS",
            "AccessLevel_ActivateOn": generate_random_AccessLevelActivateOn(),
            "AccessLevel_Deactivate": generate_random_AccessLevelDeactivateOn()
        })

    LocationInOrOut = None
    GeneralAccess = False
    ActiveBadge = False

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
        "Badge_Count": str(badge_count),
        "Badges": badges,

        # Access level data
        "AccessLvl_Count": str(accessLvl_count),
        "AccessLvl": accessLvl,

        "ProfileImg_URL": profile_image
    }

# Generate 3000 profiles
profiles = [generate_profile() for _ in range(3000)]
# Save the profiles to a JSON file
with open('Website1/my-node-server/profiles.json', 'w') as f:
    json.dump(profiles, f, indent=4)

"""# Save the profiles to a JSON file
with open('profiles.json', 'w') as f:
    json.dump(profiles, f, indent=4)"""

print("Fake dataset generated and saved to profiles.json")