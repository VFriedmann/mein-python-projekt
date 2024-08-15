from flask import Flask, render_template, request, redirect, jsonify
import sqlite3

app = Flask(__name__)

# Funktion zum Initialisieren der Datenbank
def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                comment TEXT NOT NULL,
                link TEXT NOT NULL,
                category1 TEXT NOT NULL,
                category2 TEXT NOT NULL,
                date TEXT NOT NULL
            )
        ''')
        conn.commit()

init_db()

# Route zum Rendern der Hauptseite
@app.route('/')
def index():
    return render_template('index.html')

# Route zum Hinzufügen eines Links
@app.route('/add_link', methods=['POST'])
def add_link():
    data = request.get_json()
    comment = data['comment']
    link = data['link']
    category1 = data['category1']
    category2 = data['category2']
    date = data['date']

    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO links (comment, link, category1, category2, date)
            VALUES (?, ?, ?, ?, ?)
        ''', (comment, link, category1, category2, date))
        conn.commit()
    
    return jsonify(success=True)

# Route zum Abrufen aller Links
@app.route('/get_links', methods=['GET'])
def get_links():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM links')
        links = cursor.fetchall()
    
    return jsonify(links)

# Route zum Löschen eines Links
@app.route('/delete_link', methods=['POST'])
def delete_link():
    data = request.get_json()
    link_id = data['id']

    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM links WHERE id = ?', (link_id,))
        conn.commit()

    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)
