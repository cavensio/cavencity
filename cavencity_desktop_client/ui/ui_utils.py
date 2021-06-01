def format_uptime(seconds: int) -> str:
    uptime = f'{seconds % 60}s'
    if seconds >= 60:
        uptime = f'{int(seconds % 3600 / 60)}m {uptime}'
        if seconds >= 3600:
            uptime = f'{int(seconds % 86400 / 36000)}h {uptime}'
        if seconds >= 86400:
            uptime = f'{int(seconds / 86400)}h {uptime}'
    return uptime


def format_micros(micros: int) -> str:
    if micros > 9999:
        return f'{int(micros/1000)}ms'
    else:
        return f'{micros}μs'