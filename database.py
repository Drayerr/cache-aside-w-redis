import psycopg2

from config import PG_HOST, PG_DB, PG_USER, PG_PASS, PG_PORT


# Functions
def get_db_connection():
    try:
        connection = psycopg2.connect(
            host=PG_HOST, database=PG_DB, user=PG_USER, password=PG_PASS, port=PG_PORT
        )
        # If connection went well, returns connection object.
        print("\n✅ Database connected! ")
        return connection

    except psycopg2.Error as error:
        print("\n" + "=" * 50)
        print(f"🚨 Error trying when connecting with POSTGRESQL 🚨")
        print(f"Check if the DB is running.")
        print(f"Check your credentials at config.py: {error}")
        print("=" * 50 + "\n")
        return None


# Execution
def test():
    # Connect
    print("\nAttempting to connect to the database...")
    connection = get_db_connection()
    if not connection:
        print("\n🚨 Error, exiting test.")
        return

    # Events

    # Closing connection
    try:
        connection.close()
        print("Connection closed.")
    except Exception as e:
        print(f"Error closing connection: {e}")


test()
