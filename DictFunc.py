def get_group_members(num_members):
    group_members = []

    for member in range(num_members):
        details = {
            'Name': input("Please enter Student Name: "),
            'Surname': input("Please enter Student Surname: "),
            'Project Role': input("Please enter Project Role: ")
        }
        group_members.append(details)

    return group_members

# Example usage
num_members = 6
group_members = get_group_members(num_members)
print(group_members)