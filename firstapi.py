from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Connecting to the SQLite database 
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Creating the table if it doesn't exist 
c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)''')
conn.commit()

@app.route('/adduser', methods=['POST'])
def add_user():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400

    data = request.get_json()
    name = data.get('name')
    user_id = data.get('id')

    if not all([name, user_id]):
        return jsonify({'error': 'Missing name or id'}), 400

    # Adding user to the database
    c.execute("INSERT INTO users VALUES (?, ?)", (user_id, name))
    conn.commit()

    
    c.execute("SELECT name FROM users WHERE id > 5")
    names = [row[0] for row in c.fetchall()]

    return jsonify({'names_with_ids_above_5': names})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  
