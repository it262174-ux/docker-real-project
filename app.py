from flask import Flask, jsonify
import psycopg2
import os
import time

app = Flask(__name__)


def connect_db():
    while True:
        try:
            return psycopg2.connect(
                host=os.getenv("DB_HOST"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD")
            )
        except psycopg2.OperationalError:
            print("Database not ready. Retrying...")
            time.sleep(2)


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "version": "1.1"
    })


@app.route("/visits")
def visits():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS visits (
            id SERIAL PRIMARY KEY
        )
    """)

    cursor.execute("INSERT INTO visits DEFAULT VALUES")
    cursor.execute("SELECT COUNT(*) FROM visits")

    count = cursor.fetchone()[0]

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "visits": count
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)