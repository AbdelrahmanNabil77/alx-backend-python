#!/usr/bin/env python3
from seed import connect_to_prodev

def stream_users():
    """Generator that yields user records one at a time from the user_data table."""
    connection = connect_to_prodev()
    if not connection:
        return

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row

    cursor.close()
    connection.close()
