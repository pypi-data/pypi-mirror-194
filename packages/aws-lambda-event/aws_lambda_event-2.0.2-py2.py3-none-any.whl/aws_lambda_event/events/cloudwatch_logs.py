# -*- coding: utf-8 -*-

import dataclasses
import base64

from ..base import Base


@dataclasses.dataclass
class CloudWatchLogsEvent(Base):
    awslogs: dict = dataclasses.field(default_factory=dict)

    @property
    def binary_data(self) -> bytes:
        return base64.b64decode(self.awslogs["data"].encode("utf-8"))

    @classmethod
    def fake(
        cls,
        data: str = "H4sIAAAAAAAAAHWPwQqCQBCGX0Xm7EFtK+smZBEUgXoLCdMhFtKV3akI8d0bLYmibvPPN3wz00CJxmQnTO41whwWQRIctmEcB6sQbFC3CjW3XW8kxpOpP+OC22d1Wml1qZkQGtoMsScxaczKN3plG8zlaHIta5KqWsozoTYw3/djzwhpLwivWFGHGpAFe7DL68JlBUk+l7KSN7tCOEJ4M3/qOI49vMHj+zCKdlFqLaU2ZHV2a4Ct/an0/ivdX8oYc1UVX860fQDQiMdxRQEAAA==",
    ) -> "CloudWatchLogsEvent":
        data = {"awslogs": {"data": data}}
        return cls.from_dict(data)
