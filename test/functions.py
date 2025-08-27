from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

TRANSACTIONS_TABLE = "transactions"
STATS_TABLE = "transactions_stats"

def insert_row_and_update(row):
    """Inserta una fila en la tabla transactions y actualiza las estadisticas""" 
    
    # Convert NaN to None
    row["price"] = None if pd.isna(row["price"]) else row["price"]

    with engine.begin() as conn:
        # Insertar fila en transactions
        conn.execute(text(f"""
            INSERT INTO {TRANSACTIONS_TABLE} (timestamp, price, user_id)
            VALUES (:timestamp, :price, :user_id)
        """), {
            "timestamp": row["timestamp"],
            "price": row["price"],
            "user_id": row["user_id"]
        })

        # Asignamos a price_value
        price_value = row["price"]
        

        # Obtenemos las estadisticas guardadas hasta el momento
        stats = conn.execute(text(f"SELECT total_count, valid_count, average_price, min_price, max_price FROM {STATS_TABLE} LIMIT 1")).fetchone()

        # Actualizamos las estadisticas con el nuevo row
        if stats is None:
            total_count = 1
            valid_count = 1 if price_value is not None else 0
            average_price = price_value
            min_price = price_value
            max_price = price_value
            conn.execute(text(f"""
                INSERT INTO {STATS_TABLE} (total_count, valid_count, average_price, min_price, max_price)
                VALUES (:total_count, :valid_count, :average_price, :min_price, :max_price)
            """), {
                "total_count": total_count,
                "valid_count": valid_count,
                "average_price": round(average_price,3),
                "min_price": min_price,
                "max_price": max_price
            })
            
        else:
            total_count, valid_count, average_price, min_price, max_price = stats

            total_count += 1

            if price_value is not None: # Evitamos que los Null afecten a las estadisticas
                valid_count += 1
                average_price = (average_price*(valid_count-1) + price_value)/(valid_count) # (Xavg_n = (Xavg_n-1*(n-1) + Xn)/n)
                min_price = min(min_price, price_value)
                max_price = max(max_price, price_value)

            conn.execute(text(f"""
                UPDATE {STATS_TABLE}
                SET total_count = :total_count,
                    valid_count = :valid_count,
                    average_price = :average_price,
                    min_price = :min_price,
                    max_price = :max_price
            """), {
                "total_count": total_count,
                "valid_count": valid_count,
                "average_price": round(average_price,3),
                "min_price": min_price,
                "max_price": max_price
            })

def show_stats():
    """ Muestra las estadisticas actuales """

    with engine.begin() as conn:
        stats = conn.execute(text(f"SELECT * FROM {STATS_TABLE} LIMIT 1")).fetchone()
        if stats is None:
            print("No stats available.")
        else:
            total_count, valid_count, average_price, min_price, max_price = stats
            print(f"Total Count: {total_count}")
            print(f"Average Price: {average_price}")
            print(f"Min Price: {min_price}")
            print(f"Max Price: {max_price}\n\n")

