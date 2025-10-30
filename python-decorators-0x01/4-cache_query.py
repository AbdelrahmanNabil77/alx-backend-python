#!/usr/bin/env python3
"""Module that provides a query caching decorator for database operations"""

import time
import sqlite3 
import functools
import logging
from typing import Callable, Any, Dict, Tuple, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global cache to store query results
query_cache: Dict[str, Tuple[List[Tuple], float]] = {}


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


def cache_query(func: Callable) -> Callable:
    """Decorator that caches query results to avoid redundant database calls.
    
    This decorator:
    1. Uses the SQL query string as a cache key
    2. Checks if the query result is already in the cache
    3. If in cache, returns the cached result without executing the query
    4. If not in cache, executes the query and stores the result in the cache
    
    Args:
        func: The function to decorate
        
    Returns:
        Callable: The decorated function
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Extract the query from arguments
        query = kwargs.get('query')
        if not query:
            if args and isinstance(args[0], str):
                query = args[0]
            else:
                # If no query is provided, just execute the function without caching
                logger.warning("No query provided for caching")
                return func(conn, *args, **kwargs)
        
        # Use the query string as the cache key
        cache_key = query
        
        # Check if the query result is in the cache
        if cache_key in query_cache:
            cached_result, timestamp = query_cache[cache_key]
            cache_age = time.time() - timestamp
            logger.info(f"Cache hit for query: {query[:50]}... (Age: {cache_age:.2f}s)")
            return cached_result
        
        # If not in cache, execute the query
        logger.info(f"Cache miss for query: {query[:50]}...")
        start_time = time.time()
        result = func(conn, *args, **kwargs)
        execution_time = time.time() - start_time
        
        # Store the result in the cache with a timestamp
        query_cache[cache_key] = (result, time.time())
        
        logger.info(f"Query executed in {execution_time:.4f}s and cached")
        return result
    
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
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
    
    # Demonstrate caching
    print("1. First call will execute the query and cache the result:")
    start_time = time.time()
    users = fetch_users_with_cache(query="SELECT * FROM users")
    first_call_time = time.time() - start_time
    print(f"   Result: {users}")
    print(f"   Execution time: {first_call_time:.6f} seconds")
    
    print("\n2. Second call with the same query will use the cached result:")
    start_time = time.time()
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    second_call_time = time.time() - start_time
    print(f"   Result: {users_again}")
    print(f"   Execution time: {second_call_time:.6f} seconds")
    print(f"   Speed improvement: {first_call_time / second_call_time:.2f}x faster")
    
    print("\n3. Different query will not use the cache:")
    start_time = time.time()
    filtered_users = fetch_users_with_cache(query="SELECT * FROM users WHERE id = 1")
    print(f"   Result: {filtered_users}")
    print(f"   Execution time: {time.time() - start_time:.6f} seconds")