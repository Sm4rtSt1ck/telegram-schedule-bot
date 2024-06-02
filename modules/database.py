from csv import DictReader, DictWriter


def __load_users() -> dict[int, str]:
    with open("database/users.csv", newline='', encoding='utf-8') as csvfile:
        reader = DictReader(csvfile)
        users: dict[int, str] = {}
        for row in reader:
            users[int(row["UserID"])] = row["Group"]
    return users


def rewrite_groups() -> None:
    with open("database/users.csv", 'w', newline='', encoding='utf-8') as csvfile:
        writer = DictWriter(csvfile, fieldnames=['UserID', 'Group'])
        writer.writeheader()
        
        for uid, grp in __users_groups.items():
            writer.writerow({'UserID': uid, 'Group': grp})


def check_user(userID: int) -> bool:
    return userID in __users_groups


def get_group(userID: int) -> str:
    """Safely return the user's group (if user exists)"""

    try:
        return __users_groups.get(userID)
    except KeyError:
        return None


def get_users() -> dict[int, str]:
    return __users_groups


# Users' id and their groups
__users_groups: dict[int, str] = __load_users()
