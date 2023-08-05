# -*- coding: utf-8 -*-

import typing as T
import dataclasses
from datetime import datetime

from ..helpers import datetime_from_timestamp
from ..base import Base


@dataclasses.dataclass
class CloudWatchScheduledEvent(Base):
    id: str = dataclasses.field(default=None)
    version: str = dataclasses.field(default=None)
    detail_type: str = dataclasses.field(default=None)
    source: str = dataclasses.field(default=None)
    account: str = dataclasses.field(default=None)
    time: str = dataclasses.field(default=None)
    region: str = dataclasses.field(default=None)
    resources: T.List[str] = dataclasses.field(default_factory=list)
    detail: dict = dataclasses.field(default_factory=dict)

    @classmethod
    def from_dict(
        cls, data: T.Optional[dict]
    ) -> T.Optional["CloudWatchScheduledEvent"]:
        if data is None:
            return data
        fields = cls._get_fields()
        kwargs = dict()
        for field_name in fields:
            if field_name in data:
                kwargs[field_name] = data[field_name]
        kwargs["detail_type"] = data.get("detail-type")
        return cls(**kwargs)

    @property
    def first_resource(self) -> str:
        return self.resources[0]

    @classmethod
    def fake(cls) -> "CloudWatchScheduledEvent":
        data = {
            "id": "cdc73f9d-aea9-11e3-9d5a-835b769c0d9c",
            "version": "0",
            "detail-type": "Scheduled Event",
            "source": "aws.events",
            "account": "123456789012",
            "time": "1970-01-01T00:00:00Z",
            "region": "us-east-1",
            "resources": ["arn:aws:events:us-east-1:123456789012:rule/ExampleRule"],
            "detail": {},
        }
        return cls.from_dict(data)
