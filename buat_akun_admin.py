
from akun import buat_hash
from koneksi import buka_koneksi

# INPUT DATA ADMIN
nama = input("Nama admin: ")
username = input("Username: ")
password = input("Password: ")

# MEMBUAT HASH PASSWORD
password_hash = buat_hash(password)

# MENYIMPAN DATA ADMIN
koneksi = buka_koneksi()
cursor = koneksi.cursor()

cursor.execute("""
    INSERT INTO pengguna
    (nama_pengguna, username, password_hash, id_role)
    VALUES (%s, %s, %s, 1)
""", (nama, username, password_hash))

koneksi.commit()

print("Akun admin berhasil dibuat!")

cursor.close()
koneksi.close()
