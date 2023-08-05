# -*- coding: utf-8 -*-

import typing as T
import base64
import dataclasses
from datetime import datetime

from ..helpers import datetime_from_timestamp
from ..base import Base


@dataclasses.dataclass
class KinesisFirehoseRecord(Base):
    recordId: str = dataclasses.field(default=None)
    approximateArrivalTimestamp: int = dataclasses.field(default=None)
    data: str = dataclasses.field(default=None)

    @property
    def binary_data(self) -> bytes:
        return base64.b64decode(self.data.encode("utf-8"))

    @property
    def approximate_arrival_datetime(self) -> datetime:
        return datetime_from_timestamp(self.approximateArrivalTimestamp)


@dataclasses.dataclass
class KinesisFirehoseEvent(Base):
    invocationId: T.Optional[str] = dataclasses.field(default=None)
    deliveryStreamArn: T.Optional[str] = dataclasses.field(default=None)
    region: T.Optional[str] = dataclasses.field(default=None)
    records: T.List[KinesisFirehoseRecord] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        self.records = [
            KinesisFirehoseRecord.from_dict(record) for record in self.records
        ]

    @classmethod
    def fake(
        cls,
        record_id: str = "49546986683135544286507457936321625675700192471156785154",
        data: str = "SGVsbG8sIHRoaXMgaXMgYSB0ZXN0IDEyMy4=",
        approximate_arrival_datetime: datetime = datetime(2000, 1, 1),
    ) -> "KinesisFirehoseEvent":
        data = {
            "invocationId": "invocationIdExample",
            "deliveryStreamArn": "arn:aws:kinesis:EXAMPLE",
            "region": "us-east-1",
            "records": [
                {
                    "recordId": record_id,
                    "approximateArrivalTimestamp": int(
                        approximate_arrival_datetime.timestamp() * 1000
                    ),
                    "data": data,
                }
            ],
        }
        return cls.from_dict(data)
