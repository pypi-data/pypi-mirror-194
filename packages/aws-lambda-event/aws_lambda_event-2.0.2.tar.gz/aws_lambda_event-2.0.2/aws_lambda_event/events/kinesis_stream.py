# -*- coding: utf-8 -*-

import typing as T
import base64
import dataclasses
from datetime import datetime

from ..helpers import datetime_from_timestamp
from ..base import Base


@dataclasses.dataclass
class Kinesis(Base):
    partitionKey: T.Optional[str] = dataclasses.field(default=None)
    kinesisSchemaVersion: T.Optional[str] = dataclasses.field(default=None)
    data: T.Optional[str] = dataclasses.field(default=None)
    sequenceNumber: T.Optional[str] = dataclasses.field(default=None)
    approximateArrivalTimestamp: T.Optional[int] = dataclasses.field(default=None)

    @property
    def binary_data(self) -> bytes:
        return base64.b64decode(self.data.encode("utf-8"))

    @property
    def approximate_arrival_datetime(self) -> datetime:
        return datetime_from_timestamp(self.approximateArrivalTimestamp)


@dataclasses.dataclass
class KinesisStreamRecord(Base):
    eventSource: T.Optional[str] = dataclasses.field(default=None)
    eventID: T.Optional[str] = dataclasses.field(default=None)
    invokeIdentityArn: T.Optional[str] = dataclasses.field(default=None)
    eventVersion: T.Optional[str] = dataclasses.field(default=None)
    eventName: T.Optional[str] = dataclasses.field(default=None)
    eventSourceARN: T.Optional[str] = dataclasses.field(default=None)
    awsRegion: T.Optional[str] = dataclasses.field(default=None)
    kinesis: T.Optional[Kinesis] = dataclasses.field(default=None)

    def __post_init__(self):
        self.kinesis = Kinesis.from_dict(self.kinesis)

    @property
    def kinesis_partition_key(self) -> str:
        return self.kinesis.partitionKey

    @property
    def kinesis_binary_data(self) -> bytes:
        return self.kinesis.binary_data

    @property
    def kinesis_sequence_number(self) -> str:
        return self.kinesis.sequenceNumber

    @property
    def kinesis_approximate_arrival_datetime(self) -> datetime:
        return self.kinesis.approximate_arrival_datetime


@dataclasses.dataclass
class KinesisStreamEvent(Base):
    Records: T.List[KinesisStreamRecord] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        self.Records = [
            KinesisStreamRecord.from_dict(record) for record in self.Records
        ]

    @classmethod
    def fake(
        cls,
        sequence_number: str = "49545115243490985018280067714973144582180062593244200961",
        data: str = "SGVsbG8sIHRoaXMgaXMgYSB0ZXN0IDEyMy4=",
        approximate_arrival_datetime: datetime = datetime(2000, 1, 1),
    ) -> "KinesisStreamEvent":
        data = {
            "Records": [
                {
                    "kinesis": {
                        "partitionKey": "partitionKey-03",
                        "kinesisSchemaVersion": "1.0",
                        "data": data,
                        "sequenceNumber": sequence_number,
                        "approximateArrivalTimestamp": int(
                            approximate_arrival_datetime.timestamp()
                        ),
                    },
                    "eventSource": "aws:kinesis",
                    "eventID": "shardId-000000000000:49545115243490985018280067714973144582180062593244200961",
                    "invokeIdentityArn": "arn:aws:iam::EXAMPLE",
                    "eventVersion": "1.0",
                    "eventName": "aws:kinesis:record",
                    "eventSourceARN": "arn:aws:kinesis:EXAMPLE",
                    "awsRegion": "us-east-1",
                }
            ]
        }
        return cls.from_dict(data)
