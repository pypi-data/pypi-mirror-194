import datetime


def stamp_utc_now(ms=True) -> str:
    """date and time stamp, to ms resolution: str(YYYYMMDD_HHMMSS.mss)
    or if ms==False: str(YYYYMMDD_HHMMSS)
    """
    stamp = (
        datetime.datetime.utcnow()
        .isoformat(sep="_")
        .replace(":", "")
        .replace("-", "")[:19]
    )
    if ms:
        return stamp
    else:
        return stamp.split(".")[0]
