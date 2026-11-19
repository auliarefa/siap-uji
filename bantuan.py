import psycopg2
from koneksi import buka_koneksi
import os

def clear():
    os.system('cls')

# =====================================
# FUNGSI BANTUAN
# =====================================

def garis():
    print("=" * 50)

def judul(teks):
    garis()
    print(teks.center(50))
    garis()

def jeda():
    input("\nTekan ENTER untuk kembali...")

def ambil_data(sql, data=()):
    koneksi = buka_koneksi()
    cursor = koneksi.cursor()

    try:
        cursor.execute(sql, data)
        hasil = cursor.fetchall()
        return hasil

    except psycopg2.Error as error:
        print("Terjadi kesalahan:", error)
        return []

    finally:
        cursor.close()
        koneksi.close()

def jalankan(sql, data=()):
    koneksi = buka_koneksi()
    cursor = koneksi.cursor()

    try:
        cursor.execute(sql, data)
        koneksi.commit()
        return cursor.rowcount

    except psycopg2.Error as error:
        koneksi.rollback()
        print("Terjadi kesalahan:", error)
        return 0

    finally:
        cursor.close()
        koneksi.close()
