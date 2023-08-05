from sdfspu import sdf_time


def test_stamp_utc_now_no_arg():
    stamp = sdf_time.stamp_utc_now()
    assert "_" in stamp
    assert "." in stamp
    assert len(stamp) == len("YYYYMMDD_HHMMSS.mss")


def test_stamp_utc_now_ms_false():
    stamp = sdf_time.stamp_utc_now(ms=False)
    assert "_" in stamp
    assert "." not in stamp
    assert len(stamp) == len("YYYYMMDD_HHMMSS")
