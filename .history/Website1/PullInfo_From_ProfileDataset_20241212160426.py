import json
import openpyxl

# Load the profiles.json file
with open('Website1\my-node-server\profiles.json', 'r') as file:
    profiles = json.load(file)

# Create a new Excel workbook and add a sheet
wb = openpyxl.Workbook()
sheet = wb.active
sheet.title = 'Employee IDs'

# Add header row
sheet.append(['Employee_ID'])

# Extract Employee_IDs and write them to the Excel sheet
for profile in profiles:
    sheet.append([profile['Employee_ID']])

# Save the workbook
wb.save('Employee_IDs.xlsx')
print("Employee IDs have been saved to Employee_IDs.xlsx")
