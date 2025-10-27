import psycopg2
from psycopg2.extras import RealDictCursor
from config import PG_HOST, PG_DB, PG_USER, PG_PASS, PG_PORT
from redis_cache import get_redis_connection


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
def setup_database(db_connection):
    try:
        with db_connection.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS products (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    price NUMERIC(10, 2) NOT NULL
                );
            """
            )
            db_connection.commit()
            print("[DB SETUP] Table 'products' verified/created successfully!")

    except Exception as e:
        print(f"[DB SETUP] Fail while creating table: {e}")


def insert_products(db_connection, name: str, price: float):
    try:
        with db_connection.cursor() as cur:
            cur.execute(
                "INSERT INTO products (name, price) VALUES (%s, %s);", (name, price)
            )
            db_connection.commit()
            print(f"[DB INSERT] Product '{name}' successfully inserted.")

    except Exception as e:
        print(f"[DB INSERT] Error while inserting product: {e}")
        db_connection.rollback()


def get_all_products(db_connection):
    try:
        with db_connection.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT id, name, price FROM products;")
            products = cur.fetchall()
            print(f"[DB SELECT] Total products found: {len(products)}")
            return products

    except Exception as e:
        print(f"[DB SELECT] Error while searching table items: {e}")
        return []


# Execution
def test():
    # Connect DB
    print("\nAttempting to connect to the database...")
    db_connection = get_db_connection()
    if not db_connection:
        print("\n🚨 Error, exiting test.")
        return

    # Connect Redis
    print("\nAttempting to connect to Redis...")
    redis_connection = get_redis_connection()

    # Events
    setup_database(db_connection)
    insert_products(db_connection, "smartphone", 249.99)
    get_all_products(db_connection)

    # Closing db connection
    try:
        db_connection.close()
        print("DB Connection closed.")
    except Exception as e:
        print(f"Error closing connection: {e}")

    print("Test finished.")


test()
