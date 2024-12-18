import json

# Load the profiles.json file
with open('my-node-server/profiles.json', 'r') as file:
    profiles = json.load(file)

# Extract Employee_IDs
for profile in profiles:
    if 'Employee_ID' in profile:
        print(profile['Employee_ID'])