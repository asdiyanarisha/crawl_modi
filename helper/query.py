from pymongo import TEXT, DESCENDING, HASHED, IndexModel, errors


def insert_company(db, data):
    cursor = db.cursor()
    sql = "INSERT INTO modi_perusahaan (kode_perusahaan, nama_perusahaan, badan_usaha, no_akte, tgl_akte) VALUES (%s, %s, %s, %s, %s)"
    cursor.executemany(sql, data)

    db.commit()

    return cursor.rowcount


def insert_permission(db, data):
    cursor = db.cursor()
    sql = "INSERT INTO modi_perizinan (kode_perusahaan, no_perizinan, jenis_perizinan, modi_id, tahap_kegiatan, " \
          "jenis_operasi, kode_wiup, luas_ha, tahap_cnc, tgl_mulai, tgl_berakhir, komoditas) " \
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(sql, data)

    db.commit()

    return cursor.rowcount


def insert_location(db, data):
    cursor = db.cursor()
    sql = "INSERT INTO modi_lokasi (kode_perusahaan, no_perizinan, lokasi) VALUES (%s, %s, %s)"
    cursor.executemany(sql, data)

    db.commit()

    return cursor.rowcount


def tracked_company(db, kode_perusahaan):
    cursor = db.cursor()
    sql = "SELECT * FROM modi_perusahaan WHERE kode_perusahaan = '{}'".format(kode_perusahaan)
    cursor.execute(sql)

    res = cursor.fetchone()
    return res
