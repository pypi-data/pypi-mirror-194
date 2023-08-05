# -*- coding: utf-8 -*-

from datetime import datetime, timezone

TS_MIN = 4102463
TS_2020 = 4102462800

def datetime_from_timestamp(ts: int) -> datetime:
    if ts < TS_MIN:
        raise ValueError(f"Don't support timestamp smaller than {TS_MIN}")
    if ts >= TS_2020:
        return datetime.fromtimestamp(ts / 1000, tz=timezone.utc)
    else:
        return datetime.fromtimestamp(ts, tz=timezone.utc)
