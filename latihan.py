import psycopg2

from koneksi import buka_koneksi
from bantuan import garis, judul, jeda, ambil_data, jalankan,clear              

# =====================================
# MENAMPILKAN DAFTAR MATERI
# =====================================

def tampilkan_materi():
    clear()
    judul("DAFTAR MATERI")

    daftar = ambil_data("""
        SELECT id_materi, nama_materi
        FROM materi
        ORDER BY id_materi
    """)

    print("+----+--------------------------+")
    print("| No | Nama Materi              |")
    print("+----+--------------------------+")

    for materi in daftar:
        print("| {:<2} | {:<24} |".format(
            materi[0], materi[1]
        ))

    print("+----+--------------------------+")

    return daftar


# =====================================
# PENGELOLAAN MATERI
# =====================================

def tambah_materi():
    clear()
    judul("TAMBAH MATERI")

    nama = input("Nama Materi : ")

    garis()
    print("[1] Simpan")
    print("[2] Batal")

    pilih = input("\nPilih menu: ")

    if pilih == "1":
        jalankan("""
            INSERT INTO materi (nama_materi)
            VALUES (%s)
        """, (nama,))

        print("Materi berhasil ditambahkan.")

    else:
        print("Penambahan dibatalkan.")

    jeda()


def ubah_materi():
    clear()
    judul("UBAH MATERI")

    id_materi = input("ID Materi : ")

    data = ambil_data("""
        SELECT nama_materi
        FROM materi
        WHERE id_materi = %s
    """, (id_materi,))

    if len(data) == 0:
        print("Materi tidak ditemukan.")
        jeda()
        return

    print("Nama Materi Lama:", data[0][0])

    nama_baru = input("Nama Materi Baru : ")

    garis()
    print("[1] Simpan Perubahan")
    print("[2] Batal")

    pilih = input("\nPilih menu: ")

    if pilih == "1":
        jalankan("""
            UPDATE materi
            SET nama_materi = %s
            WHERE id_materi = %s
        """, (nama_baru, id_materi))

        print("Materi berhasil diubah.")

    else:
        print("Perubahan dibatalkan.")

    jeda()


def hapus_materi():
    clear()
    judul("HAPUS MATERI")

    id_materi = input("ID Materi : ")

    data = ambil_data("""
        SELECT nama_materi
        FROM materi
        WHERE id_materi = %s
    """, (id_materi,))

    if len(data) == 0:
        print("Materi tidak ditemukan.")
        jeda()
        return

    print("Nama Materi:", data[0][0])

    print("\nApakah Anda yakin ingin menghapus materi ini?")
    print("[1] Ya, Hapus")
    print("[2] Batal")

    pilih = input("\nPilih menu: ")

    if pilih == "1":
        jalankan("""
            DELETE FROM materi
            WHERE id_materi = %s
        """, (id_materi,))

        print("Materi berhasil dihapus.")

    else:
        print("Penghapusan dibatalkan.")

    jeda()


def menu_materi():
    while True:
        clear()
        judul("PENGELOLAAN MATERI")

        print("[1] Lihat Daftar Materi")
        print("[2] Tambah Materi")
        print("[3] Ubah Materi")
        print("[4] Hapus Materi")
        print("[5] Kembali")

        pilih = input("\nPilih menu: ")

        if pilih == "1":
            tampilkan_materi()
            jeda()

        elif pilih == "2":
            tambah_materi()

        elif pilih == "3":
            tampilkan_materi()
            ubah_materi()

        elif pilih == "4":
            tampilkan_materi()
            hapus_materi()

        elif pilih == "5":
            break

        else:
            print("Pilihan tidak tersedia.")
            jeda()


# =====================================
# MENAMPILKAN DAFTAR SOAL
# =====================================

def tampilkan_daftar_soal():
    clear()
    judul("DAFTAR SOAL")

    daftar = ambil_data("""
        SELECT
            materi.id_materi,
            materi.nama_materi,
            COUNT(soal.id_soal)
        FROM materi
        LEFT JOIN soal
        ON materi.id_materi = soal.id_materi
        GROUP BY materi.id_materi, materi.nama_materi
        ORDER BY materi.id_materi
    """)

    print("+----+----------------------+----------------+")
    print("| ID | Materi               | Jumlah Soal    |")
    print("+----+----------------------+----------------+")

    for data in daftar:
        print("| {:<2} | {:<20} | {:<14} |".format(
            data[0], data[1], data[2]
        ))

    print("+----+----------------------+----------------+")

    return daftar


def lihat_soal_materi():
    clear()
    daftar = tampilkan_daftar_soal()

    if len(daftar) == 0:
        print("Belum ada materi.")
        jeda()
        return

    id_materi = input("\nID Materi: ")
    clear()

    soal = ambil_data("""
        SELECT
            id_soal, pertanyaan, pilihan_a, pilihan_b,
            pilihan_c, pilihan_d, kunci_jawaban, pembahasan
        FROM soal
        WHERE id_materi = %s
        ORDER BY id_soal
    """, (id_materi,))

    if len(soal) == 0:
        print("Belum ada soal pada materi tersebut.")

    for data in soal:
        print("\nID Soal:", data[0])
        print("Pertanyaan:", data[1])
        print("A.", data[2])
        print("B.", data[3])
        print("C.", data[4])
        print("D.", data[5])
        print("Kunci Jawaban:", data[6])
        print("Pembahasan:", data[7])

    print("\n[1] Kembali")
    input("Pilih menu: ")
    clear()


# =====================================
# TAMBAH, UBAH, DAN HAPUS SOAL
# =====================================

def tambah_soal():
    clear()
    judul("TAMBAH SOAL")

    tampilkan_materi()

    id_materi = input("\nID Materi : ")

    pertanyaan = input("Pertanyaan  : ")
    a = input("Pilihan A   : ")
    b = input("Pilihan B   : ")
    c = input("Pilihan C   : ")
    d = input("Pilihan D   : ")
    kunci = input("Kunci Jawaban (A/B/C/D) : ").upper()
    pembahasan = input("Pembahasan  : ")

    if kunci not in ["A", "B", "C", "D"]:
        print("Kunci jawaban harus A, B, C, atau D.")
        jeda()
        return

    garis()
    print("[1] Simpan Soal")
    print("[2] Batal")

    pilih = input("\nPilih menu: ")

    if pilih == "1":
        jalankan("""
            INSERT INTO soal (
                id_materi, pertanyaan, pilihan_a, pilihan_b,
                pilihan_c, pilihan_d, kunci_jawaban, pembahasan
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (id_materi, pertanyaan, a, b, c, d, kunci, pembahasan))

        print("Soal berhasil ditambahkan.")

    else:
        print("Penambahan dibatalkan.")

    jeda()


def ubah_soal():
    clear()
    judul("UBAH SOAL")

    id_soal = input("ID Soal : ")

    data = ambil_data("""
        SELECT *
        FROM soal
        WHERE id_soal = %s
    """, (id_soal,))

    if len(data) == 0:
        print("Soal tidak ditemukan.")
        jeda()
        return

    print("Data soal akan ditampilkan untuk diperbarui.")
    print("Pertanyaan Lama:", data[0][2])

    pertanyaan = input("Pertanyaan Baru      : ")
    a = input("Pilihan A Baru       : ")
    b = input("Pilihan B Baru       : ")
    c = input("Pilihan C Baru       : ")
    d = input("Pilihan D Baru       : ")
    kunci = input("Kunci Jawaban Baru   : ").upper()
    pembahasan = input("Pembahasan Baru      : ")

    if kunci not in ["A", "B", "C", "D"]:
        print("Kunci jawaban harus A, B, C, atau D.")
        jeda()
        return

    garis()
    print("[1] Simpan Perubahan")
    print("[2] Batal")

    pilih = input("\nPilih menu: ")

    if pilih == "1":
        jalankan("""
            UPDATE soal
            SET pertanyaan = %s,
                pilihan_a = %s,
                pilihan_b = %s,
                pilihan_c = %s,
                pilihan_d = %s,
                kunci_jawaban = %s,
                pembahasan = %s
            WHERE id_soal = %s
        """, (pertanyaan, a, b, c, d, kunci, pembahasan, id_soal))

        print("Soal berhasil diubah.")

    else:
        print("Perubahan dibatalkan.")

    jeda()


def hapus_soal():
    clear()
    judul("HAPUS SOAL")

    id_soal = input("ID Soal : ")

    data = ambil_data("""
        SELECT pertanyaan
        FROM soal
        WHERE id_soal = %s
    """, (id_soal,))

    if len(data) == 0:
        print("Soal tidak ditemukan.")
        jeda()
        return

    print("Pertanyaan:", data[0][0])

    print("\nApakah Anda yakin ingin menghapus soal ini?")
    print("[1] Ya, Hapus")
    print("[2] Batal")

    pilih = input("\nPilih menu: ")

    if pilih == "1":
        jalankan("""
            DELETE FROM soal
            WHERE id_soal = %s
        """, (id_soal,))

        print("Soal berhasil dihapus.")

    else:
        print("Penghapusan dibatalkan.")

    jeda()


def menu_soal():
    clear()
    while True:
        judul("PENGELOLAAN BANK SOAL")

        print("[1] Lihat Daftar Soal")
        print("[2] Tambah Soal")
        print("[3] Ubah Soal")
        print("[4] Hapus Soal")
        print("[5] Kembali")

        pilih = input("\nPilih menu: ")

        if pilih == "1":
            lihat_soal_materi()

        elif pilih == "2":
            tambah_soal()

        elif pilih == "3":
            ubah_soal()

        elif pilih == "4":
            hapus_soal()

        elif pilih == "5":
            break

        else:
            print("Pilihan tidak tersedia.")
            jeda()


# =====================================
# MENU ADMIN
# =====================================

def menu_admin():
    while True:
        clear()
        judul("MENU ADMIN")

        print("Selamat Datang, Admin!")
        print("\nKelola data yang tersedia pada SiapUji.\n")

        print("[1] Pengelolaan Materi")
        print("[2] Pengelolaan Bank Soal")
        print("[3] Logout")

        pilih = input("\nPilih menu: ")
        clear()

        if pilih == "1":
            menu_materi()

        elif pilih == "2":
            menu_soal()

        elif pilih == "3":
            print("\nApakah Anda yakin ingin logout?")
            print("[1] Ya")
            print("[2] Tidak")

            keluar = input("\nPilih menu: ")

            if keluar == "1":
                print("Berhasil logout.")
                break

        else:
            print("Pilihan tidak tersedia.")
            jeda()


# =====================================
# MENENTUKAN KATEGORI NILAI
# =====================================

def tentukan_kategori(nilai):
    if nilai >= 80:
        return "TINGGI"

    elif nilai >= 60:
        return "SEDANG"

    else:
        return "PERLU DITINGKATKAN"


# =====================================
# MENYIMPAN HASIL LATIHAN
# =====================================

def simpan_hasil(id_pengguna, id_materi, benar, salah, daftar_jawaban):
    koneksi = buka_koneksi()
    cursor = koneksi.cursor()

    jumlah_soal = benar + salah
    nilai = benar / jumlah_soal * 100

    try:
        cursor.execute("""
            INSERT INTO riwayat_latihan (
                id_pengguna, id_materi, tanggal_pengerjaan,
                jumlah_soal, jumlah_benar, jumlah_salah, nilai
            )
            VALUES (%s, %s, CURRENT_TIMESTAMP, %s, %s, %s, %s)
            RETURNING id_riwayat
        """, (id_pengguna, id_materi, jumlah_soal,
              benar, salah, nilai))

        id_riwayat = cursor.fetchone()[0]

        for jawaban in daftar_jawaban:
            cursor.execute("""
                INSERT INTO detail_latihan (
                    id_riwayat, id_soal,
                    jawaban_pengguna, status_jawaban
                )
                VALUES (%s, %s, %s, %s)
            """, (id_riwayat, jawaban[0], jawaban[1], jawaban[2]))

        koneksi.commit()
        return id_riwayat

    except psycopg2.Error as error:
        koneksi.rollback()
        print("Gagal menyimpan hasil:", error)
        return None

    finally:
        cursor.close()
        koneksi.close()


# =====================================
# MEMULAI LATIHAN
# =====================================

def mulai_latihan(id_pengguna):
    while True:
        clear()
        judul("PILIH MATERI")

        daftar = tampilkan_materi()

        print("\n[1] Pilih Materi")
        print("[2] Kembali")

        pilih = input("\nMasukkan pilihan: ")

        if pilih == "2":
            return

        if pilih != "1":
            print("Pilihan tidak tersedia.")
            jeda()
            continue

        id_materi = input("Masukkan ID Materi: ")

        materi = ambil_data("""
            SELECT nama_materi
            FROM materi
            WHERE id_materi = %s
        """, (id_materi,))

        if len(materi) == 0:
            print("Materi tidak ditemukan.")
            jeda()
            continue

        nama_materi = materi[0][0]

        soal = ambil_data("""
            SELECT
                id_soal, pertanyaan, pilihan_a, pilihan_b,
                pilihan_c, pilihan_d, kunci_jawaban, pembahasan
            FROM soal
            WHERE id_materi = %s
            ORDER BY id_soal
        """, (id_materi,))

        if len(soal) == 0:
            print("Belum ada soal untuk materi ini.")
            jeda()
            continue

        break

    benar = 0
    salah = 0
    daftar_jawaban = []

    for nomor, data in enumerate(soal, start=1):
        judul("LATIHAN SIAPUJI")

        print("Materi :", nama_materi)
        print("Soal   :", nomor, "dari", len(soal))
        print("\n" + "-" * 50)

        print(data[1])
        print("\nA.", data[2])
        print("B.", data[3])
        print("C.", data[4])
        print("D.", data[5])

        jawaban = input("\nJawaban (A/B/C/D): ").upper()

        while jawaban not in ["A", "B", "C", "D"]:
            print("Masukkan A, B, C, atau D.")
            jawaban = input("Jawaban: ").upper()

        if jawaban == data[6]:
            benar += 1
            status = True
            print("Jawaban benar!")

        else:
            salah += 1
            status = False
            print("Jawaban salah.")
            print("Kunci jawaban:", data[6])

        print("Pembahasan:", data[7])

        daftar_jawaban.append((data[0], jawaban, status))
        input("\nTekan ENTER untuk soal berikutnya...")

    id_riwayat = simpan_hasil(
        id_pengguna, id_materi, benar, salah, daftar_jawaban
    )

    jumlah_soal = len(soal)
    nilai = benar / jumlah_soal * 100
    kategori = tentukan_kategori(nilai)

    judul("HASIL LATIHAN")

    print("Materi         :", nama_materi)
    print("\nJumlah Soal    :", jumlah_soal)
    print("Jawaban Benar  :", benar)
    print("Jawaban Salah  :", salah)
    print("\nNilai          :", format(nilai, ".2f"))
    print("\nKategori Penguasaan:", kategori)

    if id_riwayat is not None:
        print("\n[1] Lihat Prioritas Belajar")
        print("[2] Kembali ke Menu Mahasiswa")

        pilih = input("\nPilih menu: ")

        if pilih == "1":
            tampilkan_prioritas(id_pengguna)
            jeda()


# =====================================
# PRIORITAS BELAJAR
# =====================================

def tampilkan_prioritas(id_pengguna):
    judul("PRIORITAS BELAJAR")

    daftar = ambil_data("""
        SELECT materi.nama_materi, AVG(riwayat_latihan.nilai)
        FROM riwayat_latihan
        JOIN materi
        ON riwayat_latihan.id_materi = materi.id_materi
        WHERE riwayat_latihan.id_pengguna = %s
        GROUP BY materi.id_materi, materi.nama_materi
        ORDER BY AVG(riwayat_latihan.nilai)
    """, (id_pengguna,))

    if len(daftar) == 0:
        print("Belum ada hasil latihan.")
        return

    print("Urutan materi berdasarkan nilai terendah:\n")

    print("+----+----------------------+-------+")

    for nomor, data in enumerate(daftar, start=1):
        print("| {:<2} | {:<20} | {:>5} |".format(
            nomor, data[0], format(float(data[1]), ".2f")
        ))

    print("+----+----------------------+-------+")

    print("\nMateri dengan nilai terendah menjadi")
    print("prioritas untuk dipelajari kembali.")

    print("\nMateri prioritas:", daftar[0][0])
