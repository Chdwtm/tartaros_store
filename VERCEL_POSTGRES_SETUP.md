# Setup Vercel Postgres

## Langkah 1: Buat Vercel Postgres Database

1. Buka dashboard Vercel: https://vercel.com/dashboard
2. Pilih project Anda (tartaros_store)
3. Pergi ke tab **Storage**
4. Klik **Create** → **Postgres**
5. Beri nama: `tartaros_db` (atau nama pilihan Anda)
6. Pilih region terdekat dengan user base Anda
7. Klik **Create**

## Langkah 2: Copy Connection String

1. Setelah database terbuat, copy **Connection String**
2. Ada 2 jenis:
   - **POSTGRES_URL_NON_POOLING** ← Gunakan ini untuk app kita
   - **POSTGRES_URL** ← Untuk connection pooling

Kita akan menggunakan `POSTGRES_URL_NON_POOLING`

## Langkah 3: Set Environment Variables di Vercel

1. Di dashboard Vercel project, pergi ke **Settings** → **Environment Variables**
2. Vercel seharusnya sudah auto-set `POSTGRES_URL_NON_POOLING` saat membuat database
3. Jika belum, tambahkan manual:
   - **Name**: `POSTGRES_URL_NON_POOLING`
   - **Value**: [paste connection string yang di-copy]
4. Klik **Add**
5. Deploy ulang project dengan klik **Redeploy**

## Langkah 4: Test Lokal (Optional)

Untuk test di lokal sebelum deploy:

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variable (Windows PowerShell)
$env:POSTGRES_URL_NON_POOLING = "postgresql://user:password@host:5432/dbname"

# Atau (Windows CMD)
set POSTGRES_URL_NON_POOLING=postgresql://user:password@host:5432/dbname

# Jalankan app
python app.py
```

## Langkah 5: Deploy ke Vercel

```bash
git add .
git commit -m "Migrate from SQLite to Vercel Postgres"
git push origin main
```

Vercel akan auto-deploy, dan environment variables akan ke-load otomatis.

## FAQ

### Database tidak terdeteksi?

- Pastikan environment variable `POSTGRES_URL_NON_POOLING` sudah di-set di Vercel
- Check di Vercel dashboard → Settings → Environment Variables
- Klik "Redeploy" setelah set environment variables

### Error "attempt to write a readonly database"?

- Ini error lama dari SQLite. Seharusnya sudah hilang dengan Postgres
- Jika masih muncul, clear browser cache dan reload

### Bagaimana backup database?

- Vercel Postgres otomatis backup
- Akses backup via Vercel dashboard → Storage → Postgres → Backups

### Bisa scale database later?

- Ya, Vercel Postgres supports vertical scaling
- Upgrade plan kapan saja dari dashboard

## Monitoring Database

1. Buka Vercel dashboard → Storage → Postgres
2. Lihat:
   - Query times
   - Storage usage
   - Connection count
   - Backups

---

**Catatan**: Semua data SQLite lama tidak akan otomatis migrate. Jika ada data penting, export dulu sebelum replace dengan Postgres.
