import datetime

def get_local_time(
    gmt_offset,
    current_utc_time=datetime.datetime.now(datetime.timezone.utc)
):
    '''
    Определение текущего времени по значению часового пояса.

    Параметры:
        - `gmt_offset`: смещение в часах относительно времени UTC;
        - `current_utc_time`: текущее время UTC.
    '''
    return (
        current_utc_time + datetime.timedelta(hours=gmt_offset)
    ).strftime('%H:%M')
