
import cv2
import numpy as np
import time

def otsu_coin_counter(image_path='image.png'):
    # Memulai perhitungan waktu komputasi
    start_time = time.time()
    
    # Membaca citra grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.GaussianBlur(img, (5, 5), 0)
    
    if img is None:
        print(f"Error: Citra '{image_path}' tidak ditemukan!")
        return

    # --- TAHAP 1: Analisis Histogram ---
    total_pixels = img.size
    counts, _ = np.histogram(img, bins=256, range=(0, 256))
    probabilities = counts / total_pixels

    print("=== TAHAP 1: ANALISIS HISTOGRAM ===")
    print(f"Total Piksel Citra: {total_pixels}\n")

    min_variance = float('inf')
    best_threshold = 0
    best_stats = {}

    print("=== TAHAP 2 - 5: PERHITUNGAN STATISTIK DAN VARIANS ===")
    print(f"{'Threshold (t)':<15} | {'Varians Dalam Kelas (Terkecil = Terbaik)'}")
    print("-" * 55)

    # --- TAHAP 2-6: Iterasi Mencari Nilai Otsu Terbaik ---
    for t in range(256):
        Wb = np.sum(probabilities[:t+1])
        Wf = np.sum(probabilities[t+1:])

        if Wb == 0 or Wf == 0:
            continue

        mean_b = np.sum(np.arange(t+1) * probabilities[:t+1]) / Wb
        mean_f = np.sum(np.arange(t+1, 256) * probabilities[t+1:]) / Wf

        var_b = np.sum(((np.arange(t+1) - mean_b) ** 2) * probabilities[:t+1]) / Wb
        var_f = np.sum(((np.arange(t+1, 256) - mean_f) ** 2) * probabilities[t+1:]) / Wf

        within_class_variance = (Wb * var_b) + (Wf * var_f)

        if t % 50 == 0:
            print(f"t = {t:<11} | Varians = {within_class_variance:.4f}")

        if within_class_variance < min_variance:
            min_variance = within_class_variance
            best_threshold = t
            best_stats = {
                'Wb': Wb, 'mean_b': mean_b, 'var_b': var_b,
                'Wf': Wf, 'mean_f': mean_f, 'var_f': var_f
            }

    print("-" * 55)
    print("\n=== TAHAP 6: KESIMPULAN OPTIMASI ===")
    print(f"Nilai Threshold Terbaik (t) : {best_threshold}")
    print(f"Nilai Varians Terkecil      : {min_variance:.4f}\n")

    # --- TAHAP 7: Mengaplikasikan Threshold ---
    # Catatan: Jika latar belakang gambarmu terang (putih) dan koin gelap, 
    # gunakan cv2.THRESH_BINARY_INV. Jika background gelap dan koin terang, gunakan cv2.THRESH_BINARY.
    # Di sini saya asumsikan koin lebih gelap dari background (umum terjadi pada foto koin di kertas/meja terang).
    _, binary_image = cv2.threshold(img, best_threshold, 255, cv2.THRESH_BINARY_INV)

    # --- TAHAP 8: Perhitungan Koin dengan Kontur ---
    # Mencari garis tepi (kontur) dari objek putih di citra biner
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    jumlah_koin = 0
    # Menggambar garis kontur asli untuk memvisualisasikan koin yang dihitung (opsional)
    img_color = cv2.imread(image_path) 
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        # Filter area: abaikan titik/noise kecil. 
        # Angka 100 bisa diperbesar atau diperkecil tergantung resolusi fotomu.
        if area > 100: 
            jumlah_koin += 1
            # Menggambar kotak hijau (bounding box) di sekitar koin yang valid
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(img_color, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Simpan hasil citra (biner dan kotak deteksi koin)
    cv2.imwrite('hasil_otsu_biner_PYONLY.png', binary_image)
    if img_color is not None:
        cv2.imwrite('hasil_deteksi_koin_PYONLY.png', img_color)

    # Menghentikan perhitungan waktu
    end_time = time.time()
    waktu_komputasi = end_time - start_time

    print("=== HASIL DETEKSI KOIN & WAKTU ===")
    print(f"Jumlah koin yang terdeteksi : {jumlah_koin} koin")
    print(f"Waktu komputasi total       : {waktu_komputasi:.4f} detik")
    print("\n[INFO] Citra biner disimpan sebagai 'hasil_otsu_biner.png'")
    print("[INFO] Citra hasil deteksi koin disimpan sebagai 'hasil_deteksi_koin_PYONLY.png'")

# Menjalankan fungsi
if __name__ == "__main__":
    otsu_coin_counter('image.png')