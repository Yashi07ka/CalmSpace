from flask import Flask, request, jsonify, send_from_directory
import sqlite3

app = Flask(__name__)


def create_database():
    connection = sqlite3.connect("calmnest.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS diary_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            mood TEXT,
            content TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS garden_plants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            problem TEXT NOT NULL,
            growth INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


create_database()


@app.route("/")
def home():
    return "🌿 CalmNest Backend is Running!"
@app.route("/<page>")
def serve_page(page):
    return send_from_directory(".", page)

@app.route("/api/garden", methods=["GET"])
def get_plants():

    connection = sqlite3.connect("calmnest.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM garden_plants")

    plants = [dict(row) for row in cursor.fetchall()]

    connection.close()

    return jsonify(plants)

@app.route("/api/garden", methods=["POST"])
def add_plant():

    data = request.get_json()

    problem = data.get("problem", "").strip()
    created_at = data.get("created_at", "")

    if not problem:
        return jsonify({"error": "Problem is required"}), 400

    connection = sqlite3.connect("calmnest.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO garden_plants
        (problem, growth, created_at)
        VALUES (?, ?, ?)
        """,
        (problem, 0, created_at)
    )

    connection.commit()

    plant_id = cursor.lastrowid

    connection.close()

    return jsonify({
        "message": "Plant saved successfully",
        "id": plant_id
    }), 201


@app.route("/api/garden/<int:plant_id>/grow", methods=["PUT"])
def grow_plant(plant_id):

    connection = sqlite3.connect("calmnest.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE garden_plants
        SET growth = growth + 1
        WHERE id = ? AND growth < 3
        """,
        (plant_id,)
    )

    connection.commit()

    cursor.execute(
        "SELECT * FROM garden_plants WHERE id = ?",
        (plant_id,)
    )

    plant = cursor.fetchone()

    connection.close()

    if not plant:
        return jsonify({"error": "Plant not found"}), 404

    return jsonify({
        "message": "Plant grown successfully",
        "id": plant[0],
        "growth": plant[2]
    })

@app.route("/api/diary", methods=["POST"])
def add_diary_entry():

    data = request.get_json()

    date = data.get("date", "")
    mood = data.get("mood", "")
    content = data.get("content", "").strip()

    if not content:
        return jsonify({
            "error": "Diary entry is required"
        }), 400

    connection = sqlite3.connect("calmnest.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO diary_entries
        (date, mood, content)
        VALUES (?, ?, ?)
        """,
        (date, mood, content)
    )

    connection.commit()

    entry_id = cursor.lastrowid

    connection.close()

    return jsonify({
        "message": "Diary entry saved successfully",
        "id": entry_id
    }), 201


@app.route("/api/diary", methods=["GET"])
def get_diary_entries():

    connection = sqlite3.connect("calmnest.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM diary_entries ORDER BY id DESC"
    )

    entries = [
        dict(row)
        for row in cursor.fetchall()
    ]

    connection.close()

    return jsonify(entries)




@app.route("/api/garden/<int:plant_id>", methods=["DELETE"])
def delete_plant(plant_id):

    connection = sqlite3.connect("calmnest.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM garden_plants WHERE id = ?",
        (plant_id,)
    )

    connection.commit()

    deleted = cursor.rowcount

    connection.close()

    if deleted == 0:
        return jsonify({
            "error": "Plant not found"
        }), 404

    return jsonify({
        "message": "Plant deleted successfully"
    })


@app.route("/api/diary/<int:entry_id>", methods=["DELETE"])
def delete_diary_entry(entry_id):

    connection = sqlite3.connect("calmnest.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM diary_entries WHERE id = ?",
        (entry_id,)
    )

    connection.commit()

    deleted = cursor.rowcount

    connection.close()

    if deleted == 0:
        return jsonify({
            "error": "Diary entry not found"
        }), 404

    return jsonify({
        "message": "Diary entry deleted successfully"
    })


if __name__ == "__main__":
    app.run(debug=True)



if __name__ == "__main__":
    app.run(debug=True)