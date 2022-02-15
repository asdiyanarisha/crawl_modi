from datetime import datetime, timedelta


def convert_string_to_date_ts(date, format):
    res_date = datetime.strptime(date, format)
    return res_date


def convert_ts_date(ts):
    res_date = datetime.fromtimestamp(ts)
    return res_date


def covert_date_local(arr_dt, am_pm=False):
    # date format array '["14", "Juli", "2016", "09:45"]'
    # arr_dt = date.split(" ")
    today = datetime.now()
    # process day
    if arr_dt[0]:
        day = arr_dt[0]
    else:
        day = str("{:02d}".format(today.day))
    # process month
    if arr_dt[1] in ['Januari', "Jan", "JANUARI"]:
        month = "01"
    elif arr_dt[1] in ['Februari', "Feb", "FEBRUARI"]:
        month = "02"
    elif arr_dt[1] in ['Maret', "Mar", "MARET"]:
        month = "03"
    elif arr_dt[1] in ['April', "Apr", "APRIL"]:
        month = "04"
    elif arr_dt[1] in ['Mei', "May", "MEI"]:
        month = "05"
    elif arr_dt[1] in ['Juni', "Jun", "JUNI"]:
        month = "06"
    elif arr_dt[1] in ['Juli', "Jul", "JULI"]:
        month = "07"
    elif arr_dt[1] in ['Agustus', "Agt", "Aug", "AGUSTUS"]:
        month = "08"
    elif arr_dt[1] in ['September', "Sept", "Sep", "SEPTEMBER"]:
        month = "09"
    elif arr_dt[1] in ['Oktober', "Okt", "OKTOBER"]:
        month = "10"
    elif arr_dt[1] in ['November', "Nov", "NOVEMBER"]:
        month = "11"
    elif arr_dt[1] in ['Desember', "Des", "DESEMBER"]:
        month = "12"
    else:
        month = str(today.month)
    # process year
    if arr_dt[2]:
        year = arr_dt[2]
    else:
        year = str(today.year)
    try:
        # process time
        if arr_dt[3]:
            time = arr_dt[3]
        else:
            time = "{}:{}".format(today.hour, today.minute)
    except Exception as e:
        time = "{}:{}".format(today.hour, today.minute)

    res_dt = "{}-{}-{} {}".format(year, month, day, time)
    if am_pm is False:
        res_date = datetime.strptime(res_dt, "%Y-%m-%d %H:%M")
    else:
        res_date = datetime.strptime(res_dt, "%Y-%m-%d %H:%M%p")
    return res_date


def day_end_timestamp(day):
    return datetime.now() - timedelta(days=int(day))


def count_end_day_es(day):
    date = datetime.now() - timedelta(days=int(day))
    return date.strftime("%Y-%m-%dT%H:%M:%S")
