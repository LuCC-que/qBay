import json
import uuid
import re
import sqlite3
from resources.tools.exceptions import InvalidUserUpdate

def update_user_checker(update_user: dict) -> None:
    print("===testing update user format checker========")

    '''
    This function is used to do the format checking of the update user
    data, the following rules will be checked:
            R3-2, R3-3, R3-4
    You can take look of the comment above to find out what is each if
    testing about
    '''
    # R3-4
    # Check user name, if none, then pop the value so it won't update
    if update_user["acc_name"] is None:
        update_user.pop("acc_name")

    # Check user name format
    elif not len(update_user["acc_name"]) > 2 and len(update_user["acc_name"]) < 20:
        raise InvalidUserUpdate(
            "User name has to be longer than "
            "2 characters and less than 20 characters.",
            "account-length")
    # R3-4
    # Check user name format
    elif not re.fullmatch(r'^\w+( +\w+)*$', update_user["acc_name"]):
        raise InvalidUserUpdate(
            "User name has to be non-empty, alphanumeric-only, " +
            "and space allowed only if it is not as the " +
            "prefix or suffix.", "account")

    # Check email, if none, then pop the value so it won't update
    if update_user["email"] is None:
        update_user.pop("email")

    # Check email format
    elif "email" not in update_user or len(update_user["email"]) == 0:
        raise InvalidUserUpdate(
            "Email cannot be empty.", "Email-Zero")

    # Check email format
    elif not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', update_user["email"]):
        raise InvalidUserUpdate(
            "The email has to follow addr-spec" +
            " defined in RFC 5322(aaa@ccc.xxx) ",
            "Email-Format")

    # Check postal code, if none, then pop the value so it won't update
    if update_user["postal_code"] is None:
        update_user.pop("postal_code")

    # R3-2, R3-3
    # Check postal code format
    elif not re.fullmatch(r'^([A-Za-z]\d[A-Za-z][-]?\d[A-Za-z]\d)',
                          update_user["postal_code"]):
        raise InvalidUserUpdate(
            "Postal code has to meet the required complexity:" +
            "non-empty, alphanumeric-only," +
            "has to be a valid Canadian postal code", "Invalid-Postal-Code")

    # Check address, if none, then pop the value so it won't update
    if update_user["address"] is None:
        update_user.pop("address")

    print("ALL-pass")


def update_user_saving(update_user, rows0: tuple) -> dict:
    """
    R2-1
    """
    # Create SQL code
    sql_update = "UPDATE Users "
    sql_where = "WHERE User_id = " + rows0[0] + " "  # Fetch the user id
    sql_set = "SET "

    # Set is where attribute + index, ex Name : Alex, so it can update the name to Alex
    for i in update_user.keys():
        sql_set += (i + " = " + update_user[i] + ', ')
    sql_set = sql_set[:-2]

    # Combine to form a complete SQL code
    sql = sql_update + sql_set + sql_where

    # connect the database
    import os
    path = os.path.dirname(os.path.abspath(__file__))
    print(path)
    connection = sqlite3.connect(path + "/../data.db")
    cursor = connection.cursor()

    # execute the sql = sql_update + sql_set + sql_where code
    cursor.execute(sql)
    connection.close()
