import psycopg2

from koneksi import buka_koneksi
from bantuan import garis, judul, jeda, clear              
from akun import registrasi, login                          
from riwayat import tampilkan_riwayat
from latihan import mulai_latihan, menu_admin

# =====================================
# MENU MAHASISWA
# =====================================

def menu_mahasiswa(data_pengguna):
    id_pengguna = data_pengguna[0]
    nama = data_pengguna[1]

    while True:
        clear()
        judul("MENU MAHASISWA")

        print("Selamat Datang,", nama)
        print("\nSilakan pilih fitur yang ingin digunakan:\n")

        print("[1] Mulai Latihan")
        print("[2] Riwayat Latihan")
        print("[3] Logout")

        pilih = input("\nPilih menu: ")

        if pilih == "1":
            mulai_latihan(id_pengguna)

        elif pilih == "2":
            tampilkan_riwayat(id_pengguna)

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
# MENU AWAL SIAPUJI
# =====================================

def menu_awal():
    while True:
        clear()
        judul("SIAPUJI")
        print("PROGRAM EVALUASI KESIAPAN UJIAN".center(50))

        print("\nSelamat Datang di SiapUji!")
        print("\nSilakan pilih menu:\n")

        print("[1] Registrasi Mahasiswa")
        print("[2] Login")
        print("[3] Keluar")

        print("\n" + "-" * 50)

        pilih = input("Pilih menu: ")

        if pilih == "1":
            registrasi()

        elif pilih == "2":
            pengguna = login()

            if pengguna is not None:
                if pengguna[2] == "Admin":
                    menu_admin()

                elif pengguna[2] == "Mahasiswa":
                    menu_mahasiswa(pengguna)

        elif pilih == "3":
            judul("SIAPUJI SELESAI")

            print("Terima kasih telah menggunakan SiapUji!")
            print("\nSemoga latihan yang dilakukan membantu")
            print("meningkatkan kesiapan ujian Anda.")

            garis()
            print("PROGRAM SELESAI".center(50))
            garis()
            break

        else:
            print("Pilihan tidak tersedia.")
            jeda()

# =====================================
# MENJALANKAN PROGRAM
# =====================================

def main():
    try:
        koneksi = buka_koneksi()
        koneksi.close()

        print("Koneksi database berhasil!")

        menu_awal()

    except psycopg2.Error as error:
        print("Koneksi database gagal:", error)


if __name__ == "__main__":
    main()