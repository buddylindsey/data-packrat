import arrow

from django.conf import settings

def get_run_times():
    start, end = settings.RUN_TIMES

    start_hour = int(start.split(':')[0])
    start_min = int(start.split(':')[1])
    end_hour = int(end.split(':')[0])
    end_min = int(end.split(':')[1])

    now = arrow.utcnow()

    start_time = now.replace(hour=start_hour, minute=start_min)
    end_time = now.replace(hour=end_hour, minute=end_min)

    if end_hour < start_hour:
        end_time = end_time.shift(days=1)

    return [start_time, end_time]

def can_run_task():
    start, end = get_run_times()

    now = arrow.utcnow()

    if now > start and now < end:
        return True
    else:
        return False
