import cv2
import ramiros_vision as rv

# 1. Buka gambar grayscale (Ubah 'koin.png' sesuai nama gambarmu)
img = cv2.imread("kopi.png", cv2.IMREAD_GRAYSCALE)

if img is None:
    print("Gambar tidak ditemukan! Pastikan nama dan lokasinya benar.")
    exit()

# 2. Jalankan fungsi Otsu dari library C kamu
# Mengembalikan nilai threshold dan gambar hasil binerisasi
nilai_threshold, img_biner = rv.otsuRams(img)
print(f"Otsu Threshold dari C: {nilai_threshold}")

# 3. Jalankan fungsi Chain Code dari gambar biner tersebut
kode_rantai = rv.chain_code(img_biner)
print(f"Panjang Rantai Code  : {len(kode_rantai)}")
print(f"Hasil Rantai Code    : {''.join(map(str, kode_rantai))}")

# 4. Tampilkan gambar hasil binerisasi buatan C kamu
cv2.imshow("Hasil Citra Biner (C)", img_biner)
cv2.waitKey(0)
cv2.destroyAllWindows()