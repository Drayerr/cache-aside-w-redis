import time

from database import (
    setup_database,
    insert_product,
    get_product_by_id,
    get_db_connection,
)
from redis_cache import get_from_cache, set_in_cache
from config import CACHE_TTL

PRODUCT_ID = 1


def get_product_data(product_id: int):
    connection = get_db_connection()

    cache_key = f"product:{product_id}"

    data = get_from_cache(cache_key)
    if data:
        print(f"[HIT] | Value: $ {float(data['price']):<6.2f} | Source: REDIS CACHE")
        return data

    data = get_product_by_id(connection, product_id)
    if not (data):
        print(f"[ERROR] | Product {product_id} not found")
        return None
    if data:
        set_in_cache(cache_key, data)
        print(
            f"[MISS] | Value: $ {data['price']:<6.2f} | Source: Original DB (Not cached)"
        )
        return data


if __name__ == "__main__":
    connection = get_db_connection()
    setup_database(connection)

    insert_product(connection, "Laptop", 500.00)

    TOTAL_TIME = 30

    print("\n" + "=" * 80)
    print(f"  INIT: CACHE ASIDE TEST | TTL: {CACHE_TTL}s | DURATION: {TOTAL_TIME}s")
    print("=" * 80)
    print(
        "  -> Change the product value on DB ID 1 after the first [MISS] to see the changes."
    )
    print("=" * 80)

    start_time = time.time()
    end_time = start_time + TOTAL_TIME

    while time.time() < end_time:
        current_time = round(time.time() - start_time, 1)
        print(f"[{current_time:>4}s]", end=" | ")

        get_product_data(PRODUCT_ID)

        time.sleep(1)

    print("\n" + "=" * 80)
    print("TEST FINISHED")
