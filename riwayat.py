from bantuan import judul, jeda, ambil_data

# =====================================
# RIWAYAT LATIHAN
# =====================================

def tampilkan_riwayat(id_pengguna):
    judul("RIWAYAT LATIHAN")

    daftar = ambil_data("""
        SELECT
            riwayat_latihan.id_riwayat,
            materi.nama_materi,
            riwayat_latihan.tanggal_pengerjaan,
            riwayat_latihan.nilai
        FROM riwayat_latihan
        JOIN materi
        ON riwayat_latihan.id_materi = materi.id_materi
        WHERE riwayat_latihan.id_pengguna = %s
        ORDER BY riwayat_latihan.tanggal_pengerjaan
    """, (id_pengguna,))

    if len(daftar) == 0:
        print("Belum ada riwayat latihan.")
        jeda()
        return

    print("Berikut riwayat latihan Anda:\n")
    print("+----+----------------------+------------+-------+")

    for nomor, data in enumerate(daftar, start=1):
        tanggal = data[2].strftime("%d-%m-%Y")

        print("| {:<2} | {:<20} | {:<10} | {:>5} |".format(
            nomor, data[1], tanggal, format(float(data[3]), ".2f")
        ))

    print("+----+----------------------+------------+-------+")

    print("\n[1] Lihat Detail Riwayat")
    print("[2] Kembali")

    pilih = input("\nPilih menu: ")

    if pilih == "1":
        id_riwayat = input("Masukkan ID Riwayat: ")

        detail_riwayat(id_pengguna, id_riwayat)

    elif pilih == "2":
        return


def detail_riwayat(id_pengguna, id_riwayat):
    judul("DETAIL RIWAYAT LATIHAN")

    data = ambil_data("""
        SELECT
            riwayat_latihan.id_riwayat,
            materi.nama_materi,
            riwayat_latihan.tanggal_pengerjaan,
            riwayat_latihan.jumlah_soal,
            riwayat_latihan.jumlah_benar,
            riwayat_latihan.jumlah_salah,
            riwayat_latihan.nilai
        FROM riwayat_latihan
        JOIN materi
        ON riwayat_latihan.id_materi = materi.id_materi
        WHERE riwayat_latihan.id_riwayat = %s
        AND riwayat_latihan.id_pengguna = %s
    """, (id_riwayat, id_pengguna))

    if len(data) == 0:
        print("Riwayat tidak ditemukan.")
        jeda()
        return

    riwayat = data[0]

    print("ID Riwayat      :", riwayat[0])
    print("Materi          :", riwayat[1])
    print("Tanggal         :", riwayat[2].strftime("%d-%m-%Y"))
    print("\nJumlah Soal     :", riwayat[3])
    print("Jawaban Benar   :", riwayat[4])
    print("Jawaban Salah   :", riwayat[5])
    print("Nilai           :", format(float(riwayat[6]), ".2f"))

    print("\n[1] Kembali ke Riwayat Latihan")
    input("\nPilih menu: ")