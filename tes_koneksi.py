from koneksi import buka_koneksi

koneksi = buka_koneksi()

print("Berhasil terhubung ke database SIAPUJI!")

koneksi.close()

koneksi = buka_koneksi()
cursor = koneksi.cursor()

koneksi = buka_koneksi()
cursor = koneksi.cursor()

cursor.execute("""
    SELECT
        soal.pertanyaan,
        soal.pilihan_a,
        soal.pilihan_b,
        soal.pilihan_c,
        soal.pilihan_d,
        soal.kunci,
        soal.pembahasan
    FROM soal
    JOIN materi
    ON soal.id_materi = materi.id_materi
    WHERE materi.nama_materi = 'Tipe Data dan Variabel'
""")

data_soal = cursor.fetchall()

for nomor, soal in enumerate(data_soal, start=1):
    print("\n" + "=" * 50)
    print("SOAL", nomor)
    print("=" * 50)

    print("Pertanyaan :", soal[0])
    print("A          :", soal[1])
    print("B          :", soal[2])
    print("C          :", soal[3])
    print("D          :", soal[4])
    print("Kunci      :", soal[5])
    print("Pembahasan :", soal[6])


cursor.close()
koneksi.close()