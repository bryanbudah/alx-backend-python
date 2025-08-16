import sqlite3
import functools
import time

def log_queries(func):
    """Decorator that logs SQL queries and execution details"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query from either args or kwargs
        query = kwargs.get('query', args[0] if args else None)
        
        if not query:
            print("Warning: No query provided")
            return func(*args, **kwargs)
            
        print(f"Executing query: {query}")
        start_time = time.perf_counter()
        
        try:
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start_time
            print(f"Query executed successfully in {elapsed:.4f} seconds")
            print(f"Returned {len(result)} rows")
            return result
        except sqlite3.Error as e:
            print(f"Query failed: {str(e)}")
            raise
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            raise
            
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Example usage
users = fetch_all_users(query="SELECT * FROM users")