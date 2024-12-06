from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Banco de dados inicial
def init_db():
    conn = sqlite3.connect("mental_health.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mood REAL,
            activities TEXT,
            sleep_hours REAL,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()

# Inicializar banco de dados
init_db()

# Endpoint para adicionar entradas
@app.route("/add_entry", methods=["POST"])
def add_entry():
    data = request.get_json()
    mood = data.get("mood")
    activities = data.get("activities")
    sleep_hours = data.get("sleep_hours")
    date = data.get("date")

    conn = sqlite3.connect("mental_health.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO entries (mood, activities, sleep_hours, date)
        VALUES (?, ?, ?, ?)
    """, (mood, activities, sleep_hours, date))
    conn.commit()
    conn.close()

    return jsonify({"message": "Entrada adicionada com sucesso!"})

# Endpoint para obter todas as entradas
@app.route("/get_entries", methods=["GET"])
def get_entries():
    conn = sqlite3.connect("mental_health.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM entries")
    entries = cursor.fetchall()
    conn.close()

    return jsonify(entries)

# Endpoint para calcular a média de humor
@app.route("/get_average_mood", methods=["GET"])
def get_average_mood():
    conn = sqlite3.connect("mental_health.db")
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(mood) FROM entries")
    average = cursor.fetchone()[0]
    conn.close()

    if average is None:
        return jsonify({"average_mood": None, "message": "Nenhuma entrada encontrada."})

    return jsonify({"average_mood": average})

# Endpoint para obter o melhor dia
@app.route("/get_best_day", methods=["GET"])
def get_best_day():
    conn = sqlite3.connect("mental_health.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM entries")
    entries = cursor.fetchall()
    conn.close()

    if not entries:
        return jsonify({"best_day": None, "message": "Nenhuma entrada registrada."})

    best_day = None
    best_score = -float("inf")

    for entry in entries:
        day_id, mood, activities, sleep_hours, date = entry
        # Calcular o score
        sleep_factor = 1 - abs(8 - sleep_hours) / 8
        score = mood * sleep_factor

        # Atualizar o melhor dia com base no maior score
        if score > best_score:
            best_score = score
            best_day = {
                "date": date,
                "mood": mood,
                "activities": activities,
                "sleep_hours": sleep_hours
            }

    return jsonify({"best_day": best_day, "message": "Melhor dia encontrado com base no humor e sono."})

if __name__ == "__main__":
    app.run(debug=True)
