# Dokumentasi API Backend Sistem Informasi Perpustakaan

Base URL: `https://perpus-backend-seven.vercel.app`

## Daftar Endpoints

### 1. Root / Cek Status
- **URL:** `/`
- **Method:** `GET`
- **Deskripsi:** Mengecek koneksi server API.
- **Contoh Respon:**
  ```json
  {
    "message": "Selamat datang di API Backend Sistem Informasi Perpustakaan!",
    "status": "success"
  }
