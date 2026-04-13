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

## Troubleshooting

### Error: "Gagal memuat data dari server"

- Pastikan server Flask sudah jalan: `python app.py`
- Cek apakah port 5000 sudah terpakai
- Jika error CORS, sudah di-handle dengan `flask-cors`

### Database Error

- Hapus file `tartaros.db` jika rusak
- Server akan membuat database baru otomatis

## Default Items

Database sudah berisi 4 item default:

1. Mythical Chest - Rp 1000 / 800
2. Clan Reroll - Rp 1000 / 1000
3. Aura Crate - Rp 250 / 1
4. Cosmetic Crate - Rp 150 / 1
