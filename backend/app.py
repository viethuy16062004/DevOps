import os
import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

PORT = int(os.environ.get("PORT", 5000))
DB_URL = os.environ.get("DB_URL")

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"})

@app.route('/about', methods=['GET'])
def about():
    return jsonify({
        "ho_ten": "Trần Việt Huy", 
        "mssv": "2251220239",
        "email": "huy_2251220239@dau.edu.vn",
        "truong": "Đại học Kiến trúc Đà Nẵng"
    })

def get_db_connection():
    return psycopg2.connect(DB_URL)

@app.route('/users', methods=['GET', 'POST'])
def manage_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (id serial PRIMARY KEY, name varchar(100) NOT NULL);''')
    conn.commit()

    if request.method == 'POST':
        data = request.get_json()
        cur.execute('INSERT INTO users (name) VALUES (%s)', (data['name'],))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "User added successfully!"}), 201
    else:
        cur.execute('SELECT id, name FROM users;')
        users = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([{"id": row[0], "name": row[1]} for row in users])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)