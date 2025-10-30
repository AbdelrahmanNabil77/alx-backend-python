#!/usr/bin/env python3
"""Module that provides a decorator for automatic database connection handling"""

import sqlite3 
import functools
from typing import Callable, Any


def with_db_connection(func: Callable) -> Callable:
    """Decorator that automatically handles opening and closing database connections.
    
    This decorator:
    1. Opens a database connection
    2. Passes the connection as the first argument to the decorated function
    3. Closes the connection after the function execution
    4. Allows the decorated function to be called without providing the connection
    
    Args:
        func: The function to decorate
        
    Returns:
        Callable: The decorated function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Open a database connection
        conn = sqlite3.connect('users.db')
        
        try:
            # Pass the connection as the first argument
            result = func(conn, *args, **kwargs)
            return result
        finally:
            # Ensure the connection is closed even if an exception occurs
            conn.close()
    
    return wrapper


@with_db_connection 
def get_user_by_id(conn, user_id): 
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
    return cursor.fetchone() 


if __name__ == "__main__":
    # Create test database and table
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Create users table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL
    )
    ''')
    
    # Insert test user if not exists
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (?, ?, ?)", 
                  (1, "John Doe", "john@example.com"))
    conn.commit()
    conn.close()
    
    # Fetch user by ID with automatic connection handling 
    user = get_user_by_id(user_id=1)
    print(user)