# Tartaros Store - CRUD dengan Python Flask + SQLite

## Struktur Aplikasi

- `index.html` - Frontend (HTML statis)
- `app.py` - Backend (Flask + SQLite)
- `tartaros.db` - Database (akan dibuat otomatis)

## Setup & Instalasi

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Atau install manual:

```bash
pip install Flask==2.3.3 flask-cors==4.0.0
```

### 2. Jalankan Server

```bash
python app.py
```

Server akan berjalan di: `http://localhost:5000`

### 3. Buka Browser

Buka file `index.html` di browser Anda (atau buka `http://localhost:5000`)

## Fitur CRUD

### CREATE (Tambah Item)

- Klik tombol "+ Tambah Item"
- Isi data: Nama, Harga Paket, Isi per Paket
- Klik "Simpan" - Data disimpan ke database

### READ (Lihat Item)

- Semua item dari database ditampilkan di tabel
- Data dimuat otomatis saat halaman dibuka/direload

### UPDATE (Edit Jumlah)

- Ubah jumlah paket di kolom "Jumlah Paket"
- Total item dan total harga otomatis ter-update

### DELETE (Hapus Item)

- Klik tombol "X" di kolom Aksi
- Konfirmasi untuk menghapus item dari database

## Endpoint API

| Method | Endpoint          | Keterangan       |
| ------ | ----------------- | ---------------- |
| GET    | `/api/items`      | Get semua items  |
| GET    | `/api/items/<id>` | Get item by ID   |
| POST   | `/api/items`      | Create item baru |
| PUT    | `/api/items/<id>` | Update item      |
| DELETE | `/api/items/<id>` | Delete item      |

## Deployment (Production)

### Deploy ke Render atau Platform Lain

Aplikasi sudah siap untuk di-publish! Berikut langkahnya:

#### 1. Persiapan Git

```bash
git init
git add .
git commit -m "Tartaros Store - Ready for production"
```

#### 2. Push ke GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/tartaros-store.git
git branch -M main
git push -u origin main
```

#### 3. Deploy ke Render.com

1. Buka https://render.com
2. Sign up dengan GitHub account
3. Klik "New" → "Web Service"
4. Pilih repository `tartaros-store`
5. Isi konfigurasi:
   - **Name**: tartaros-store
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Klik "Create Web Service"

Aplikasi akan live di URL yang diberikan Render (misal: `https://tartaros-store.onrender.com`)

### Hosting Alternatif

- **Heroku**, **Railway**, **Fly.io** - Support Python & Procfile
- **Vercel + Python Runtime** - Butuh konfigurasi tambahan
- **VPS/Server sendiri** - Gunakan `gunicorn` atau `uwsgi`

## Troubleshooting

### Error: "Gagal memuat data dari server"

- **Development**: Pastikan server Flask sudah jalan: `python app.py`
- **Production**: Cek logs di platform deployment (Render, Heroku, dll)
- Cek apakah port 5000 sudah terpakai
- CORS sudah di-handle dengan `flask-cors` ✓

### Database Error

- Hapus file `tartaros.db` jika rusak
- Server akan membuat database baru otomatis saat startup

### Health Check

Untuk test apakah server berjalan:

```bash
curl http://YOUR_DOMAIN/health
```

## Default Items

Database sudah berisi 4 item default:

1. Mythical Chest - Rp 1000 / 800
2. Clan Reroll - Rp 1000 / 1000
3. Aura Crate - Rp 250 / 1
4. Cosmetic Crate - Rp 150 / 1
