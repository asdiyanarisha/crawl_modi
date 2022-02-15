import os
import re

from helper import http_request, query
from lib import log, database
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

from bs4 import BeautifulSoup

logger = log.get_logger("crawl_modi")

headers = {
  'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0',
  'Accept': '*/*',
  'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip, deflate, br',
  'X-Requested-With': 'XMLHttpRequest',
  'Connection': 'keep-alive',
  'Referer': 'https://modi.esdm.go.id/portal/dataPerusahaan'
}


def get_profile(raw):
    table = raw.select_one("div#profile > div.example > div.example-preview > div.row > div.col-md-9 > table")
    return table.select("tr")


def get_permission(raw):
    div_table = raw.select_one("div#perizinan > div.example > div.example-preview > div.table-responsive")
    t_head = div_table.select_one("thead")
    t_body = div_table.select_one("tbody")
    data = {"row": t_body.select("tr"), "column": [cleansing_column(u) for u in t_head.select("th")]}
    return data


def cleansing_column(col):
    cl_br = re.sub(r'<br\/>', ' ', str(col))
    return re.sub(r'<.*?>', ' ', str(cl_br)).strip()


def get_company_name(raw):
    tds = raw[1].select("td")
    return re.sub(r'<.*?>', '', str(tds[1]))


def get_type_business(raw):
    tds = raw[2].select("td")
    return re.sub(r'<.*?>', '', str(tds[1]))


def get_certificate_number(raw):
    tds = raw[3].select("td")
    cer_num = re.sub(r'<.*?>', '', str(tds[1]))
    return cer_num if cer_num != "" else None


def get_certificate_date(raw):
    tds = raw[4].select("td")
    cer_date = re.sub(r'<.*?>', '', str(tds[1]))
    cer_date = cer_date if cer_date != "" else None
    if not cer_date:
        return cer_date

    return datetime.strptime(cer_date, "%Y-%m-%d")


def extract_data(index, data):
    return re.sub(r'<.*?>', "", str(data[index])).strip()


def extract_location(index, data):
    return [re.sub(r'<.*?>', '', str(u)) for u in data[index].select("li")]


def extract_area(index, data):
    area = re.sub(r'<.*?>', "", str(data[index])).strip()
    if "." in area:
        return float(area.replace(',', ''))

    return float(area.replace(',', '.'))


def extract_commodity(column, data):
    idx = None

    if "Komoditas" in column:
        idx = column.index('Komoditas')

    if "Jenis Komoditas" in column:
        idx = column.index('Jenis Komoditas')

    if not idx:
        return None

    return re.sub(r'<.*?>', "", str(data[idx])).strip()


def extract_data_permission(column, data):
    modi_id = extract_data(column.index('MODI ID'), data) if "MODI ID" in column else None
    no_perizinan = extract_data(column.index('Nomor Perizinan'), data) if "Nomor Perizinan" in column else None
    jenis_perizinan = extract_data(column.index('Jenis Perizinan'), data) if "Jenis Perizinan" in column else None
    tahap_kegiatan = extract_data(column.index('Tahapan Kegiatan'), data) if 'Tahapan Kegiatan' in column else None
    jenis_operasi = extract_data(column.index('Jenis Operasi'), data) if 'Jenis Operasi' in column else None
    kode_wiup = extract_data(column.index('Kode WIUP'), data) if 'Kode WIUP' in column else None
    luas = extract_area(column.index('Luas(ha)'), data) if 'Luas(ha)' in column else 0
    tahap_cnc = extract_data(column.index('Tahapan CNC'), data) if 'Tahapan CNC' in column else None
    tgl_mulai = extract_data(column.index('Tgl Mulai Berlaku'), data) if 'Tgl Mulai Berlaku' in column else None
    tgl_berakhir = extract_data(column.index('Tgl Berakhir'), data) if 'Tgl Berakhir' in column else None
    location = extract_location(column.index('Lokasi'), data) if 'Lokasi' in column else []
    komoditas = extract_commodity(column, data)
    return {
        "modi_id": modi_id, "no_perizinan": no_perizinan, "jenis_perizinan": jenis_perizinan,
        "tahap_kegiatan": tahap_kegiatan, "jenis_operasi": jenis_operasi, "kode_wiup": kode_wiup, "luas_ha": luas,
        "tahap_cnc": tahap_cnc, "tgl_mulai": datetime.strptime(tgl_mulai, "%Y-%m-%d"),
        "tgl_berakhir": datetime.strptime(tgl_berakhir, "%Y-%m-%d"), "lokasi": location, "komoditas": komoditas
    }


def process_crawl(url, raw):
    db = database.db_connect()

    kode_perusahaan = re.sub(r'https.*\/|\?.*', "", url)
    res = query.tracked_company(db, kode_perusahaan)

    bs_raw = BeautifulSoup(raw, 'html.parser')
    profile_tag = get_profile(bs_raw)

    nama_perusahaan = get_company_name(profile_tag)
    badan_usaha = get_type_business(profile_tag)
    no_akte = get_certificate_number(profile_tag)
    tgl_akte = get_certificate_date(profile_tag)

    permission = []
    location = []

    result = get_permission(bs_raw)
    for row_pms in result['row']:
        r_per = extract_data_permission(result['column'], row_pms.select("td"))
        permission.append((
            kode_perusahaan, r_per['no_perizinan'], r_per['jenis_perizinan'], r_per['modi_id'], r_per['tahap_kegiatan'],
            r_per['jenis_operasi'], r_per['kode_wiup'], r_per['luas_ha'], r_per['tahap_cnc'], r_per['tgl_mulai'],
            r_per['tgl_berakhir'], r_per['komoditas']
        ))
        for loc in r_per['lokasi']:
            location.append((
                kode_perusahaan, r_per['no_perizinan'], loc
            ))

    if not res:
        query.insert_company(db, [(kode_perusahaan, nama_perusahaan, badan_usaha, no_akte, tgl_akte)])
        query.insert_permission(db, permission)
        query.insert_location(db, location)
        print("Success Insert {} : {}".format(url, nama_perusahaan))
    else:
        print("Already Tracked {} ".format(url))


def detail(url):
    try:
        res = http_request.html_get(url, headers=headers)
        if not res:
            logger.error("Error get data")

        process_crawl(url, res)
    except Exception as e:
        logger.error("URL {} : {}".format(url, str(e)))


def main():
    page = int(os.environ.get('START_PAGE'))
    retry = 5
    while True:
        try:
            url = "https://modi.esdm.go.id/portal/dataPerusahaan/getdata?page={}&sortby=id&sorttype=asc&perusahaan=&" \
                  "noakte=".format(page)
            res = http_request.html_get(url, headers=headers)
            if not res:
                logger.error("Error get data")

            bs_res = BeautifulSoup(res, 'html.parser')
            tr_s = bs_res.select('tr')
            for tr in tr_s:
                if "pagination" in str(tr):
                    continue

                a_href = tr.select_one('td > a')
                company_url = a_href['href']
                detail(company_url)

            retry = 0
            page += 1
        except Exception as e:
            logger.error("Error Crawl {}".format(str(e)))
            retry += 1
            if retry == 3:
                break


if __name__ == '__main__':
    main()
