#!/usr/bin/env python3
"""Module that provides decorators for database operations with retry functionality"""

import time
import sqlite3 
import functools
import logging
from typing import Callable, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


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


def retry_on_failure(retries: int = 3, delay: int = 2) -> Callable:
    """Decorator that retries a function if it raises an exception.
    
    This decorator:
    1. Executes the decorated function
    2. If the function raises an exception, it waits for the specified delay
    3. Retries the function up to the specified number of retries
    4. If all retries fail, it raises the last exception
    
    Args:
        retries: Number of times to retry the function (default: 3)
        delay: Number of seconds to wait between retries (default: 2)
        
    Returns:
        Callable: A decorator function
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            attempts = 0
            last_exception: Optional[Exception] = None
            
            while attempts <= retries:
                try:
                    # Attempt to execute the function
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    last_exception = e
                    
                    if attempts <= retries:
                        # Log the exception and retry
                        logger.warning(
                            f"Attempt {attempts}/{retries} failed for {func.__name__}: {str(e)}"
                            f" - Retrying in {delay} seconds..."
                        )
                        # Wait before retrying
                        time.sleep(delay)
                    else:
                        # Log the final failure
                        logger.error(
                            f"All {retries} retries failed for {func.__name__}: {str(e)}"
                        )
                        # Re-raise the last exception
                        raise last_exception
        
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


# Add a function that simulates transient database errors
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def simulate_transient_failure(conn):
    # Counter to track the number of attempts
    # We'll use a global variable for simplicity in this example
    if not hasattr(simulate_transient_failure, "attempts"):
        simulate_transient_failure.attempts = 0
    
    # Increase the attempt counter
    simulate_transient_failure.attempts += 1
    
    # Simulate a transient error for the first two attempts
    if simulate_transient_failure.attempts <= 2:
        # Simulate a database error (e.g., temporary connection issue)
        raise sqlite3.OperationalError("Simulated transient error: database is locked")
    
    # On the third attempt, perform the query successfully
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


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
    
    # Insert test users if not exists
    test_users = [
        (1, "John Doe", "john@example.com"),
        (2, "Jane Smith", "jane@example.com"),
        (3, "Bob Johnson", "bob@example.com")
    ]
    
    for user in test_users:
        cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (?, ?, ?)", user)
    
    conn.commit()
    conn.close()
    
    print("1. Regular fetch without simulated errors:")
    users = fetch_users_with_retry()
    print(users)
    
    print("\n2. Fetch with simulated transient errors:")
    print("   (This should retry and succeed after 2 failures)")
    users = simulate_transient_failure()
    print(f"   Success on 3rd attempt: {users}")