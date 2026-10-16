import os

import psycopg2
import psycopg2.extras
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)
DATABASE_URL = os.environ["DATABASE_URL"]
WEB_SERVICE_URL = os.environ["WEB_SERVICE_URL"]
STATUSES = {"planned", "playing", "completed"}


def query(sql, params=(), fetch=True):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params)
            return cur.fetchall() if fetch else None


def serialize(rows):
    return [{k: (float(v) if k == "min_cpu_ghz" else v.isoformat() if k == "added_at" else v)
             for k, v in r.items()} for r in rows]


@app.get("/api/library")
def get_library():
    return jsonify(serialize(query("SELECT * FROM library ORDER BY added_at DESC, id DESC")))


@app.post("/api/library")
def add_to_library():
    g = request.get_json(force=True)
    try:
        rows = query(
            """INSERT INTO library (game_id, title, genre, min_ram_gb, min_cpu_ghz, min_gpu, min_disk_gb)
               VALUES (%(id)s, %(title)s, %(genre)s, %(min_ram_gb)s, %(min_cpu_ghz)s, %(min_gpu)s, %(min_disk_gb)s)
               ON CONFLICT (game_id) DO NOTHING RETURNING *""", g)
    except (KeyError, psycopg2.Error) as e:
        return jsonify(error=str(e)), 400
    if not rows:
        return jsonify(error="Игра уже в библиотеке"), 409
    return jsonify(serialize(rows)[0]), 201


@app.put("/api/library/<int:item_id>")
def update_status(item_id):
    status = (request.get_json(force=True) or {}).get("status")
    if status not in STATUSES:
        return jsonify(error="invalid status"), 400
    rows = query("UPDATE library SET status=%s WHERE id=%s RETURNING *", (status, item_id))
    return (jsonify(serialize(rows)[0]), 200) if rows else (jsonify(error="not found"), 404)


@app.delete("/api/library/<int:item_id>")
def delete_item(item_id):
    query("DELETE FROM library WHERE id=%s", (item_id,), fetch=False)
    return "", 204


@app.get("/api/genres")
def genres():
    return _proxy("/genres")


@app.get("/api/catalog")
def catalog():
    return _proxy("/games", request.args)


def _proxy(path, params=None):
    try:
        r = requests.get(WEB_SERVICE_URL + path, params=params, timeout=5)
        r.raise_for_status()
        return jsonify(r.json())
    except requests.RequestException as e:
        return jsonify(error=f"web-service unavailable: {e}"), 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
