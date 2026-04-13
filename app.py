from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Database setup
DB_PATH = 'tartaros.db'
PORT = int(os.environ.get('PORT', 5000))

def init_db():
    """Inisialisasi database"""
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price INTEGER NOT NULL,
                pack INTEGER NOT NULL
            )
        ''')
        # Insert default items
        default_items = [
            ('Mythical Chest', 1000, 800),
            ('Clan Reroll', 1000, 1000),
            ('Aura Crate', 250, 1),
            ('Cosmetic Crate', 150, 1)
        ]
        c.executemany('INSERT INTO items (name, price, pack) VALUES (?, ?, ?)', default_items)
        conn.commit()
        conn.close()

def get_db_connection():
    """Membuka koneksi database"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ============= API ENDPOINTS =============

# GET all items
@app.route('/api/items', methods=['GET'])
def get_items():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    return jsonify([dict(item) for item in items])

# GET single item
@app.route('/api/items/<int:id>', methods=['GET'])
def get_item(id):
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM items WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if item is None:
        return jsonify({'error': 'Item tidak ditemukan'}), 404
    return jsonify(dict(item))

# CREATE new item
@app.route('/api/items', methods=['POST'])
def create_item():
    data = request.get_json()
    
    if not all(k in data for k in ['name', 'price', 'pack']):
        return jsonify({'error': 'Data tidak lengkap'}), 400
    
    conn = get_db_connection()
    conn.execute('INSERT INTO items (name, price, pack) VALUES (?, ?, ?)',
                 (data['name'], data['price'], data['pack']))
    conn.commit()
    item_id = conn.lastrowid
    conn.close()
    
    return jsonify({'id': item_id, **data}), 201

# UPDATE item
@app.route('/api/items/<int:id>', methods=['PUT'])
def update_item(id):
    data = request.get_json()
    
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM items WHERE id = ?', (id,)).fetchone()
    
    if item is None:
        conn.close()
        return jsonify({'error': 'Item tidak ditemukan'}), 404
    
    name = data.get('name', item['name'])
    price = data.get('price', item['price'])
    pack = data.get('pack', item['pack'])
    
    conn.execute('UPDATE items SET name = ?, price = ?, pack = ? WHERE id = ?',
                 (name, price, pack, id))
    conn.commit()
    conn.close()
    
    return jsonify({'id': id, 'name': name, 'price': price, 'pack': pack})

# DELETE item
@app.route('/api/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM items WHERE id = ?', (id,)).fetchone()
    
    if item is None:
        conn.close()
        return jsonify({'error': 'Item tidak ditemukan'}), 404
    
    conn.execute('DELETE FROM items WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Item berhasil dihapus'}), 200

# ============= SERVE STATIC FILES =============
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=False, port=PORT, host='0.0.0.0')
