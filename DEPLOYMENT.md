# 🚀 Deploy ke Render.com

## Langkah 1: Siapkan GitHub Repository

### A. Install Git (jika belum)

```bash
# Download dari https://git-scm.com/
```

### B. Initialize Git Repository

```bash
cd C:\Users\Cesa\Documents\CESA\KULIAH\Tartaros
git init
git add .
git commit -m "Initial commit - Tartaros Store CRUD"
```

### C. Buat GitHub Repository

1. Buka https://github.com/new
2. Isi nama repo: `tartaros-store`
3. Jangan pilih README/gitignore (sudah ada)
4. Klik "Create repository"

### D. Push ke GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/tartaros-store.git
git branch -M main
git push -u origin main
```

**Ganti `YOUR_USERNAME` dengan username GitHub Anda!**

---

## Langkah 2: Deploy ke Render

### A. Sign Up di Render

1. Buka https://render.com
2. Klik "Sign up"
3. Pilih "Continue with GitHub"
4. Authorize Render untuk akses repository Anda

### B. Create New Web Service

1. Dashboard Render → klik "New" → "Web Service"
2. Connect repository → pilih `tartaros-store`
3. Isi konfigurasi:
   - **Name**: `tartaros-store`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Region**: `Singapore` (terdekat Indonesia)
   - **Plan**: `Free` ✅

### C. Build & Deploy

1. Klik "Create Web Service"
2. Render akan otomatis build & deploy
3. Tunggu sampai berwarna hijau "Live" (5-10 menit)
4. Catat domain Anda: `https://tartaros-store-xxxxx.onrender.com`

---

## Langkah 3: Update Variabel (Optional)

Jika ingin custom environment variables:

1. Di dashboard Render → Web Service Anda
2. Tab "Environment"
3. Klik "Add Environment Variable"
4. Contoh:
   - `FLASK_ENV`: `production`
   - `FLASK_DEBUG`: `0`

---

## ✅ Selesai!

Aplikasi Anda sekarang live di:

```
https://tartaros-store-xxxxx.onrender.com
```

### Testing:

- Buka domain di browser
- Coba tambah, edit, delete item
- Data disimpan di SQLite Render
- Print struk ✓

---

## 📝 Notes

### Database Persistent?

- ✅ YES! SQLite disimpan di Render filesystem
- Data akan hilang jika upgrade ke Render free tier yang berbeda
- Upgrade ke "Starter" plan ($7/bulan) untuk persistent

### Updating Code?

Tinggal push ke GitHub, Render otomatis redeploy dalam 2-5 menit

```bash
git add .
git commit -m "Update: [apa yang diubah]"
git push
```

### Sleep Mode?

- Free tier: Aplikasi sleep jika 15 min idle (first request lambat)
- Upgrade ke Starter jika perlu always-on

---

## 🆘 Troubleshooting

### "Application Error"

- Cek logs di Render dashboard
- Pastikan `Procfile` ada
- Pastikan `requirements.txt` lengkap

### Database hilang setelah deploy ulang

- Upgrade ke paid plan atau backup manual

### API 404

- Cek console browser (F12 → Console)
- API_URL sudah otomatis resolve ke domain Render

---

Butuh bantuan? Chat aku! 👍
