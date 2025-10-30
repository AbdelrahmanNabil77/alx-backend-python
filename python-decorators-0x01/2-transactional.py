#!/usr/bin/env python3
"""Module that provides decorators for database connection and transaction handling"""

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


def transactional(func: Callable) -> Callable:
    """Decorator that manages database transactions.
    
    This decorator:
    1. Starts a transaction by disabling autocommit mode
    2. Executes the function within the transaction
    3. Commits the transaction if the function completes successfully
    4. Rolls back the transaction if an exception occurs
    
    Args:
        func: The function to decorate
        
    Returns:
        Callable: The decorated function
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            # Execute the function within a transaction
            result = func(conn, *args, **kwargs)
            
            # If no exception occurs, commit the transaction
            conn.commit()
            return result
        except Exception as e:
            # If an exception occurs, roll back the transaction
            conn.rollback()
            # Re-raise the exception to be handled by the caller
            raise e
    
    return wrapper


@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))


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
    
    # Check current email
    cursor.execute("SELECT email FROM users WHERE id = ?", (1,))
    print(f"Current email: {cursor.fetchone()[0]}")
    conn.close()
    
    # Update user's email with automatic transaction handling 
    update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
    
    # Verify the update
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM users WHERE id = ?", (1,))
    print(f"Updated email: {cursor.fetchone()[0]}")
    conn.close()