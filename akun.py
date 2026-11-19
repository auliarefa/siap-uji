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
        clear()
        judul("REGISTRASI MAHASISWA")

        print("Silakan isi data berikut:\n")

        nama = input("Nama Lengkap : ")
        username = input("Username     : ")
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
            jeda()
            break

        elif pilih == "2":
            break

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
