from flask import Flask, jsonify, request
import threading
from flask_cors import CORS
from modules.sweep import sweep
import sqlite3
import uuid

# ====================================
# ============= SETUP ================
# ====================================

backend = Flask(__name__)
CORS(backend) # Enable CORS for your Flask app. This should fix the preflight issue.

DATABASE = 'amplifiers.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS amplifiers (
                id TEXT PRIMARY KEY, -- Changed to TEXT for UUIDs
                name TEXT NOT NULL,
                channel_count INTEGER NOT NULL
            )
        ''')
        conn.commit()

# Initialize the database when the app starts
init_db()

@backend.route('/', methods=['GET'])
def welcome():
    return jsonify({"message": "Welcome, this API is up and running!"}), 200


# ====================================
# ============= DB API ===============
# ====================================

# Add Amplifiers
@backend.route('/amplifiers', methods=['POST'])
def add_amplifier():
    data = request.get_json()
    if not data or 'name' not in data or 'channel_count' not in data:
        return jsonify({"error": "Missing name or channel_count"}), 400

    name = data['name']
    channel_count = data['channel_count']
    new_id = str(uuid.uuid4()) # Generate a UUID and convert it to string

    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            # Insert the generated UUID along with other data
            cursor.execute("INSERT INTO amplifiers (id, name, channel_count) VALUES (?, ?, ?)", (new_id, name, channel_count))
            conn.commit()
            return jsonify({"message": "Amplifier added successfully", "id": new_id, "name": name, "channel_count": channel_count}), 201
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

# List Amplifiers
@backend.route('/amplifiers', methods=['GET'])
def get_amplifiers():
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, channel_count FROM amplifiers")
            amplifiers = []
            for row in cursor.fetchall():
                amplifiers.append({"id": row[0], "name": row[1], "channel_count": row[2]})
            return jsonify(amplifiers), 200
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

# Get Amplifier by ID
@backend.route('/amplifiers/<string:amplifier_id>', methods=['GET']) # Changed to string for UUID
def get_amplifier(amplifier_id):
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, channel_count FROM amplifiers WHERE id = ?", (amplifier_id,))
            amplifier = cursor.fetchone()
            if amplifier:
                return jsonify({"id": amplifier[0], "name": amplifier[1], "channel_count": amplifier[2]}), 200
            else:
                return jsonify({"error": "Amplifier not found"}), 404
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

# Update Amplfier by ID
@backend.route('/amplifiers/<string:amplifier_id>', methods=['PUT']) # Changed to string for UUID
def update_amplifier(amplifier_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided for update"}), 400

    name = data.get('name')
    channel_count = data.get('channel_count')

    if not name and channel_count is None: # Corrected condition for channel_count
        return jsonify({"error": "No fields to update (name or channel_count required)"}), 400

    update_fields = []
    update_values = []

    if name:
        update_fields.append("name = ?")
        update_values.append(name)
    if channel_count is not None:
        update_fields.append("channel_count = ?")
        update_values.append(channel_count)

    update_values.append(amplifier_id)

    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute(f"UPDATE amplifiers SET {', '.join(update_fields)} WHERE id = ?", tuple(update_values))
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({"error": "Amplifier not found"}), 404
            return jsonify({"message": "Amplifier updated successfully", "id": amplifier_id}), 200
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

# Remove Amplifier by ID
@backend.route('/amplifiers/<string:amplifier_id>', methods=['DELETE']) # Changed to string for UUID
def delete_amplifier(amplifier_id):
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM amplifiers WHERE id = ?", (amplifier_id,))
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({"error": "Amplifier not found"}), 404
            return jsonify({"message": "Amplifier deleted successfully", "id": amplifier_id}), 200
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

# ====================================
# ============ TESTING ===============
# ====================================

# Code here for testing amp, prob will call function that does the gpio handeling, than other code that does the processing, then return this data on the display.

# ====================================
# ============== MAIN ================
# ====================================

@backend.route('/sweep', methods=['POST'])
def play_sweep():
    sweep_thread = threading.Thread(
        target=sweep,
        args=(20, 20000, 3, 44100)
    )
    sweep_thread.start()

    return jsonify({"message": "Sine sweep"}), 200


@backend.route('/test', methods=['POST'])
def test_amp():
    data = request.get_json()
    amplifier_id = data.get('id')
    if not amplifier_id:
        return jsonify({"error": "Missing amplifier id"}), 400

    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, channel_count FROM amplifiers WHERE id = ?", (amplifier_id,))
            amplifier = cursor.fetchone()
            if amplifier:
                for i in range(amplifier[2]):
                    print(f"Channel {i}:")
                    sweep(20, 20000, 0.5, 44100)

                return jsonify({"message": f"Amplifier testing complete! (id={amplifier[0]}, channel count={amplifier[2]})"}), 200
            else:
                return jsonify({"error": "Amplifier not found"}), 404
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    backend.run(host='0.0.0.0', port=5001, debug=True)
