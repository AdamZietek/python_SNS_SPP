from datetime import date

def data_count(year, month, day, hour, mins, seconds):
    dday=date.toordinal(date(year, month, day)) - date.toordinal(date(1980, 1, 6)) + hour/24 + mins/1440 + seconds/86400

    return int(dday / 7), (dday % 7) * 86400
