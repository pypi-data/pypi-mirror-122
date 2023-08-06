"""Metadata configuration."""
import functools
import zoneinfo

import tzlocal


@functools.lru_cache()
def tz() -> zoneinfo.ZoneInfo:
    """Return timezone to parse naive timestamps with."""
    return tzlocal.reload_localzone()  # type: ignore
