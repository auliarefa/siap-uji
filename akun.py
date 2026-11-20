import hashlib
import secrets
from bantuan import garis, judul, jeda, ambil_data, jalankan, clear

# =====================================
# PASSWORD
# =====================================

def buat_hash(password):
    salt = secrets.token_hex(16)

    hasil = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        100000
    )

    return salt + ":" + hasil.hex()


def periksa_password(password, password_hash):
    salt, hash_asli = password_hash.split(":")

    hasil = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        100000
    )

    return hasil.hex() == hash_asli

# =====================================
# REGISTRASI MAHASISWA
# =====================================

def registrasi():
    while True:
        while True:
            clear()
            judul("REGISTRASI MAHASISWA")

            print("Silakan isi data berikut:\n")

            nama = input("Nama Lengkap : ").strip()

            if not nama:
                print("Nama tidak boleh kosong.")
                jeda()
                continue

            if not all(huruf.isalpha() or huruf == " " for huruf in nama):
                print("Nama hanya boleh berisi huruf dan spasi.")
                jeda()
                continue

            nama = nama.title()
            break

        clear()

        pesan_error = ""

        while True:
            clear()
            judul("REGISTRASI MAHASISWA")

            print("Silakan isi data berikut:\n")
            print("Ketentuan Username:")
            print("- Minimal 4 karakter")
            print("- Maksimal 20 karakter")
            print("- Menggunakan huruf, angka, dan underscore (_)")
            print("- Tidak boleh menggunakan spasi\n")

            print("Nama Lengkap :", nama)

            username = input("Username     : ").strip()

            if not username:
                pesan_error = "Username tidak boleh kosong."

            elif len(username) < 4 or len(username) > 20:
                pesan_error = "Username harus terdiri dari 4-20 karakter."

            elif any(huruf.isspace() for huruf in username):
                pesan_error = "Username tidak boleh menggunakan spasi."

            elif not username.replace("_", "").isalnum():
                pesan_error = "Username hanya boleh berisi huruf, angka, dan underscore (_)."

            else:
                break

            print(pesan_error)
            input("Tekan ENTER untuk mencoba lagi...")
            continue
        
        password = input("Password     : ")

        garis()
        print("[1] Daftar")
        print("[2] Kembali")

        pilih = input("\nPilih menu: ")

        if pilih == "1":
            username_ada = ambil_data("""
                SELECT id_pengguna
                FROM pengguna
                WHERE username = %s
            """, (username,))

            if len(username_ada) > 0:
                print("Username sudah digunakan.")
                jeda()
                continue

            role = ambil_data("""
                SELECT id_role
                FROM role_pengguna
                WHERE nama_role = 'Mahasiswa'
            """)

            if len(role) == 0:
                print("Role Mahasiswa belum tersedia.")
                jeda()
                return

            password_hash = buat_hash(password)

            jalankan("""
                INSERT INTO pengguna
                (nama_pengguna, username, password_hash, id_role)
                VALUES (%s, %s, %s, %s)
            """, (nama, username, password_hash, role[0][0]))

            print("Registrasi berhasil!")
            input("\nTekan ENTER untuk melanjutkan ke login...")
            return True
        
        elif pilih == "2":
            return False

        else:
            print("Pilihan tidak tersedia.")
            jeda()


# =====================================
# LOGIN
# =====================================

def login():
    clear()
    judul("LOGIN SIAPUJI")

    print("Masukkan data akun Anda:\n")

    username = input("Username : ")
    password = input("Password : ")

    garis()
    print("[1] Login")
    print("[2] Kembali")

    pilih = input("\nPilih menu: ")

    if pilih == "2":
        return None

    if pilih != "1":
        print("Pilihan tidak tersedia.")
        jeda()
        return None

    data = ambil_data("""
        SELECT
            pengguna.id_pengguna,
            pengguna.nama_pengguna,
            pengguna.password_hash,
            role_pengguna.nama_role
        FROM pengguna
        JOIN role_pengguna
        ON pengguna.id_role = role_pengguna.id_role
        WHERE pengguna.username = %s
    """, (username,))

    if len(data) == 0:
        print("Username tidak ditemukan.")
        jeda()
        return None

    if periksa_password(password, data[0][2]):
        print("Login berhasil!")
        return (data[0][0], data[0][1], data[0][3])

    print("Password salah.")
    jeda()
    return None
