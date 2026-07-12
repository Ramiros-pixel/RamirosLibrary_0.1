# 👁️ Ramiros Vision (`ramiros_vision`)

**Ramiros Vision** adalah pustaka (*library*) pemrosesan citra hibrida (Python & C) yang dirancang untuk performa tinggi. Pustaka ini memadukan kemudahan antarmuka Python dengan kecepatan komputasi bahasa C murni.

Repositori ini mendistribusikan versi *Pre-compiled Binary* (sudah dikompilasi menjadi `.dll`), sehingga kamu bisa langsung menggunakannya tanpa perlu melakukan kompilasi ulang. Pustaka ini berjalan berdampingan dengan OpenCV untuk manajemen *input/output* gambar.

---

## ✨ Fitur Utama
* 🚀 **Performa Tinggi:** Algoritma komputasi berat (Otsu & Chain Code) diproses di level bahasa mesin (C).
* 🐍 **Pythonic:** Mudah digunakan di Python tanpa kerumitan *pointer* memori.
* 📦 **Plug & Play:** Terdistribusi dalam bentuk *Dynamic Link Library* (.dll) yang siap di-install secara lokal.

---

## 🛠️ Prasyarat Sistem
Sebelum menginstal, pastikan komputermu memenuhi spesifikasi berikut:
1. **Sistem Operasi:** Windows 64-bit (Wajib, karena menggunakan format `.dll`).
2. **Python:** Versi 3.x (64-bit).
3. **OpenCV Python:** Digunakan untuk membaca gambar. Install via terminal: `pip install opencv-python`.

---

## 🚀 Cara Instalasi (Clone & Install)

Ikuti 2 langkah mudah ini untuk memasang `ramiros_vision` di laptopmu:

### 1. Clone Repository
Buka terminal/PowerShell, lalu unduh repositori ini:
```bash
git clone https://github.com/Ramiros-pixel/RamirosLibrary_0.1
cd RAMIROS_PACK

Kemudian install library lokal dengan menggunakan perintah 
pip install -e .
