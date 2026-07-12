import ctypes
import numpy as np
import cv2
import time
import os

# 1. Load C Library
lib_path = os.path.abspath("./Ramiros.dll")
lib_c = ctypes.CDLL(lib_path)

# 2. Definisikan argument dan return value fungsi C
# argtypes: [pointer input, total_pixel, pointer output]

lib_c.process_otsu.argtypes = [
    ctypes.POINTER(ctypes.c_ubyte), 
    ctypes.c_int, 
    ctypes.POINTER(ctypes.c_ubyte)
]

lib_c.process_otsu.restype = ctypes.c_int

def otsu_coin_counter_c(image_path='image.png'):
    start_time = time.time()
    
    # Membaca citra grayscale & blur
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Error: Citra '{image_path}' tidak ditemukan!")
        return
        
    img_blur = cv2.GaussianBlur(img, (5, 5), 0)
    
    # Ambil info ukuran gambar
    height, width = img.shape
    total_pixels = img.size
    
    # Flatten array untuk dikirim ke C
    flat_img = img_blur.flatten()
    
    # Siapkan array kosong di Python untuk menampung hasil biner dari C
    flat_output = np.zeros(total_pixels, dtype=np.uint8)
    
    # Konversi array numpy ke pointer C
    ptr_input = flat_img.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte))
    ptr_output = flat_output.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte))
    
    print("=== PROSES DI LAPISAN BAHASA C ===")
    # 3. PANGGIL FUNGSI C (Otsu & Binerisasi diproses instan di C)
    best_threshold = lib_c.process_otsu(ptr_input, total_pixels, ptr_output)
    
    print(f"Nilai Threshold Terbaik (t) dari C : {best_threshold}")
    
    # Kembalikan bentuk array output dari 1D menjadi 2D gambar kembali
    binary_image = flat_output.reshape((height, width))
    
    # --- TAHAP 8: Perhitungan Koin dengan Kontur di Python ---
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    jumlah_koin = 0
    img_color = cv2.imread(image_path)
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 100: 
            jumlah_koin += 1
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.drawContours(img_color, [cnt], -1, (255, 0, 0), 1)

    
    
    # Simpan hasil citra
    cv2.imwrite('hasil_otsu_biner.png', binary_image)
    if img_color is not None:
        cv2.imwrite('hasil_deteksi_koin.png', img_color)

    end_time = time.time()
    waktu_komputasi = end_time - start_time

    print("\n=== HASIL DETEKSI KOIN & WAKTU ===")
    print(f"Jumlah koin yang terdeteksi : {jumlah_koin} koin")
    print(f"Waktu komputasi total (C+Py): {waktu_komputasi:.4f} detik")

if __name__ == "__main__":
    # Jalankan perintah pembuka path temporary kemarin jika terminal baru dibuka kembali
    # $env:Path = "C:\Users\Asus\Downloads\w64devkit\bin;" + $env:Path
    otsu_coin_counter_c('image.png')