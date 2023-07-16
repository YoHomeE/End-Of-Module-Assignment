import json
import pickle

group_members = []

for member in range(6):
    details = {
        'Name': input("Please enter Student Name: "),
        'Surname': input("Please enter Student Surname: "),
        'Project Role': input("Please enter Project Role: ")
    }
    group_members.append(details)
print(group_members)

selection = input("Please Select Pickle Format: JSON, XML or Binary : ")
if selection == "JSON":
    with open("group-members.txt", 'w') as jsonfile:
        jsonfile.write(json.dumps(group_members))
        print("Succesfully loaded dictionairy as JSON")
    with open("group-members.txt", 'r') as jsonfile:
        contents = jsonfile.read()
        print(contents)
elif selection == "Binary":
    with open("group-members.pkl", 'wb') as binfile:
        pickle.dump(group_members, binfile)
        print('Dictionary Succesfully saved as Binary File')
    with open("group-members.pkl", 'rb') as binfile:
        contents = binfile.read()
        print(contents)
"""
elif selection == "XML":
    with open






# pip3 install dicttoxml dict2xml
group_members = {}
for member in range(6):
    inpt_name = input("Please enter Student Name: ")
    proj_role = input("Their Project Role: ")
    group_members[inpt_name] = proj_role

print(group_members"""