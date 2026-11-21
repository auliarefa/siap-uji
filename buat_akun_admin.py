from akun import buat_hash
from koneksi import buka_koneksi
from bantuan import clear,garis, judul, jeda, ambil_data, jalankan

# INPUT DATA ADMIN
def registrasi_admin():
    while True:
        while True:
            clear()
            judul("REGISTRASI ADMIN")

            print("Silakan isi data berikut:\n")

            nama = input("Nama Lengkap : ").strip()

            if not nama:
                print("\nNama tidak boleh kosong.")
                jeda()
                continue

            if not all(huruf.isalpha() or huruf == " " for huruf in nama):
                print("\nNama hanya boleh berisi huruf dan spasi.")
                jeda()
                continue

            nama = nama.title()
            break

        clear()

        pesan_error = ""

        while True:
            clear()
            judul("REGISTRASI ADMIN")

            print("Silakan isi data berikut:\n")
            print("Ketentuan Username:")
            print("- Diharuskan 4-20 karakter")
            print("- Mengandung minimal 1 huruf")
            print("- Menggunakan huruf, angka, dan underscore (_)")
            print("- Tidak boleh menggunakan spasi\n")

            print("Nama Lengkap :", nama)

            username = input("Username     : ").strip()

            if not username:
                pesan_error = "Username tidak boleh kosong."

            elif len(username) < 4 or len(username) > 20:
                pesan_error = "Username harus terdiri dari 4-20 karakter."

            elif not any(huruf.isalpha() for huruf in username):
                pesan_error = "Username harus mengandung minimal satu huruf."

            elif any(huruf.isspace() for huruf in username):
                pesan_error = "Username tidak boleh menggunakan spasi."

            elif not username.replace("_", "").isalnum():
                pesan_error = "Username hanya boleh berisi huruf, angka, dan underscore (_)."

            else:
                username_ada = ambil_data("""
                    SELECT id_pengguna
                    FROM pengguna
                    WHERE username = %s
                """, (username,))


                if len(username_ada) > 0:
                    pesan_error = "Username sudah digunakan."

                else:
                    break
        
            print("\n" + pesan_error)
            input("\nTekan ENTER untuk mencoba lagi...")
        

        while True:
            clear()
            judul("REGISTRASI ADMIN")
            print("Silakan isi data berikut:")
            print("\nKetentuan Password:")
            print("- Terdiri dari 6-20 karakter")
            print("- Mengandung minimal 1 huruf besar (A-Z)")
            print("- Mengandung minimal 1 huruf kecil (a-z)")
            print("- Mengandung minimal 1 angka atau simbol")
            print("- Tidak boleh menggunakan spasi\n")

            print("Nama Lengkap :", nama)
            print("Username :", username)

            password = input("Password     : ")

            if not password:
                pesan_error = "password tidak boleh kosong."

            elif len(password) < 6 or len(password) > 20:
                pesan_error = "Password harus terdiri dari 6-20 karakter."

            elif not any(huruf.isupper() for huruf in password):
                pesan_error = "Password harus mengandung minimal 1 huruf besar."

            elif not any(huruf.islower() for huruf in password):
                pesan_error = "Password harus mengandung minimal 1 huruf kecil."

            elif any(huruf.isspace() for huruf in password):
                pesan_error = "Password tidak boleh menggunakan spasi."

            elif not any(huruf.isdigit() or not huruf.isalnum() for huruf in password):
                pesan_error = "Password harus mengandung minimal 1 angka atau simbol."

            else:
                break

            print("\n" + pesan_error)
            input("\nTekan ENTER untuk mencoba lagi...")

        garis()
        print("[1] Daftar")

        pilih = input("\nPilih menu: ")

        if pilih == "1":
            role = ambil_data("""
                SELECT id_role
                FROM role_pengguna
                WHERE nama_role = 'Admin'
            """)

            if len(role) == 0:
                print("Role Admin belum tersedia.")
                jeda()
                return

            password_hash = buat_hash(password)

            jalankan("""
                INSERT INTO pengguna
                (nama_pengguna, username, password_hash, id_role)
                VALUES (%s, %s, %s, %s)
            """, (nama, username, password_hash, role[0][0]))

            print("Registrasi berhasil!")
            input("\nAkun admin telah dibuat")

        else:
            print("Pilihan tidak tersedia.")
            jeda()

if __name__ == "__main__":
    registrasi_admin()