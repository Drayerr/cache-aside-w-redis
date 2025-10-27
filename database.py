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


# Creates products table if not exists.
def setup_database(connection):
    try:
        with connection.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS products (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    price NUMERIC(10, 2) NOT NULL
                );
            """
            )
            connection.commit()
            print("[DB SETUP] Table 'products' verified/created successfully!")

    except Exception as e:
        print(f"[DB SETUP] Fail while creating table: {e}")


def insert_products(connection, name: str, price: float):
    try:
        with connection.cursor() as cur:
            cur.execute(
                "INSERT INTO products (name, price) VALUES (%s, %s);", (name, price)
            )
            connection.commit()
            print(f"[DB INSERT] Product '{name}' successfully inserted.")

    except Exception as e:
        print(f"[DB INSERT] Error while inserting product: {e}")
        connection.rollback()


# Execution
def test():
    # Connect
    print("\nAttempting to connect to the database...")
    connection = get_db_connection()
    if not connection:
        print("\n🚨 Error, exiting test.")
        return

    # Events
    setup_database(connection)
    insert_products(connection, "laptop", 499.99)

    # Closing connection
    try:
        connection.close()
        print("Connection closed.")
    except Exception as e:
        print(f"Error closing connection: {e}")


test()
