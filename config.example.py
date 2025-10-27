# config.py

# --- POSTGRES CONFIG ---
PG_HOST = "localhost"
PG_PORT = "5432"
PG_DB = "cache_aside_db"  # put your db name
PG_USER = "USER"  # put your username
PG_PASS = "DB_PASSWORD"  # insert password if your db have one

# --- REDIS CONFIG ---
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0  # default Redis db is zero

# --- CACHE ---
CACHE_TTL = 60  # cache live time in seconds
