from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import logging

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database setup - Vercel Postgres
DATABASE_URL = os.environ.get('POSTGRES_URL_NON_POOLING')
if not DATABASE_URL:
    # Fallback untuk development
    DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://user:password@localhost/tartaros')

PORT = int(os.environ.get('PORT', 5000))

def init_db():
    """Inisialisasi database PostgreSQL"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables 
                WHERE table_name = 'items'
            )
        """)
        table_exists = cursor.fetchone()[0]
        
        if not table_exists:
            cursor.execute('''
                CREATE TABLE items (
                    id SERIAL PRIMARY KEY,
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
                ('Cosmetic Crate', 150, 1),
                ('Passive Shard', 1000, 1000),
                ('Power Shard', 1000, 2000)
            ]
            cursor.executemany(
                'INSERT INTO items (name, price, pack) VALUES (%s, %s, %s)',
                default_items
            )
            conn.commit()
            logger.info("Database initialized successfully")
        else:
            logger.info("Database already exists")
        
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        raise

def get_db_connection():
    """Membuka koneksi database PostgreSQL"""
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# ============= API ENDPOINTS =============

# GET all items
@app.route('/api/items', methods=['GET'])
def get_items():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('SELECT * FROM items ORDER BY id')
        items = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify([dict(item) for item in items])
    except Exception as e:
        logger.error(f"Error fetching items: {e}")
        return jsonify({'error': 'Gagal memuat data dari database'}), 500

# GET single item
@app.route('/api/items/<int:id>', methods=['GET'])
def get_item(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('SELECT * FROM items WHERE id = %s', (id,))
        item = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if item is None:
            return jsonify({'error': 'Item tidak ditemukan'}), 404
        return jsonify(dict(item))
    except Exception as e:
        logger.error(f"Error fetching item: {e}")
        return jsonify({'error': 'Gagal memuat item'}), 500

# CREATE new item
@app.route('/api/items', methods=['POST'])
def create_item():
    try:
        data = request.get_json()
        
        if not all(k in data for k in ['name', 'price', 'pack']):
            return jsonify({'error': 'Data tidak lengkap'}), 400
        
        # Validasi dan konversi data
        name = str(data['name']).strip()
        try:
            price = int(data['price'])
            pack = int(data['pack'])
        except (ValueError, TypeError):
            return jsonify({'error': 'Harga dan pack harus berupa angka'}), 400
        
        if not name:
            return jsonify({'error': 'Nama item tidak boleh kosong'}), 400
        
        if price <= 0 or pack <= 0:
            return jsonify({'error': 'Harga dan pack harus lebih besar dari 0'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO items (name, price, pack) VALUES (%s, %s, %s)',
                     (name, price, pack))
        conn.commit()
        
        # Get the last inserted ID
        cursor.execute('SELECT LASTVAL()')
        item_id = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        logger.info(f"Item created successfully with ID: {item_id}, name: {name}, price: {price}, pack: {pack}")
        return jsonify({'id': item_id, 'name': name, 'price': price, 'pack': pack}), 201
    except Exception as e:
        logger.error(f"Error creating item: {e}", exc_info=True)
        return jsonify({'error': f'Gagal menambahkan item: {str(e)}'}), 500

# UPDATE item
@app.route('/api/items/<int:id>', methods=['PUT'])
def update_item(id):
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('SELECT * FROM items WHERE id = %s', (id,))
        item = cursor.fetchone()
        
        if item is None:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Item tidak ditemukan'}), 404
        
        # Get values from request, with fallback to existing values
        name = data.get('name', item['name'])
        price = data.get('price', item['price'])
        pack = data.get('pack', item['pack'])
        
        # Validasi dan konversi data
        name = str(name).strip()
        try:
            price = int(price)
            pack = int(pack)
        except (ValueError, TypeError):
            cursor.close()
            conn.close()
            return jsonify({'error': 'Harga dan pack harus berupa angka'}), 400
        
        if not name:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Nama item tidak boleh kosong'}), 400
        
        if price <= 0 or pack <= 0:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Harga dan pack harus lebih besar dari 0'}), 400
        
        cursor.execute('UPDATE items SET name = %s, price = %s, pack = %s WHERE id = %s',
                     (name, price, pack, id))
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"Item updated successfully: id={id}, name={name}, price={price}, pack={pack}")
        return jsonify({'id': id, 'name': name, 'price': price, 'pack': pack})
    except Exception as e:
        logger.error(f"Error updating item: {e}", exc_info=True)
        return jsonify({'error': f'Gagal update item: {str(e)}'}), 500

# DELETE item
@app.route('/api/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('SELECT * FROM items WHERE id = %s', (id,))
        item = cursor.fetchone()
        
        if item is None:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Item tidak ditemukan'}), 404
        
        cursor.execute('DELETE FROM items WHERE id = %s', (id,))
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"Item deleted successfully: id={id}")
        return jsonify({'message': 'Item berhasil dihapus'}), 200
    except Exception as e:
        logger.error(f"Error deleting item: {e}")
        return jsonify({'error': 'Gagal menghapus item'}), 500

# ============= SERVE STATIC FILES =============
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute('SELECT 1')
        cursor.close()
        conn.close()
        return jsonify({'status': 'ok', 'database': 'connected'}), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({'status': 'error', 'database': 'disconnected'}), 500

if __name__ == '__main__':
    try:
        init_db()
        logger.info(f"Starting server on port {PORT}")
        # Disable debug mode for production
        app.run(debug=False, port=PORT, host='0.0.0.0')
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        raise