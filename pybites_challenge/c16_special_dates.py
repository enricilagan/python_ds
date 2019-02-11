from datetime import datetime, timedelta

PYBITES_BORN = datetime(year=2016, month=12, day=19)

def gen_special_pybites_dates():
    dates = PYBITES_BORN
    dts = PYBITES_BORN
    year = 2017
    lst = []
    while dates < datetime(year = 2020, month = 1, day=1):
        dates = dates + timedelta(days=1)
        if dates == dts + timedelta(days=100):
            lst.append(dates)
            dts = dts + timedelta(days=100)
        if dates == datetime(year, 12, 19):
            lst.append(dates)
            year += 1
    return lst
