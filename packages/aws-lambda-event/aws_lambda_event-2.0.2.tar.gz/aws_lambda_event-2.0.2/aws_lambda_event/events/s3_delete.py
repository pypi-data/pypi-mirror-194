# -*- coding: utf-8 -*-

import typing as T
import dataclasses
from datetime import datetime

from ..base import Base


@dataclasses.dataclass
class OwnerIdentify(Base):
    principalId: T.Optional[str] = dataclasses.field(default=None)


@dataclasses.dataclass
class Bucket(Base):
    name: T.Optional[str] = dataclasses.field(default=None)
    arn: T.Optional[str] = dataclasses.field(default=None)
    ownerIdentity: T.Optional[OwnerIdentify] = dataclasses.field(default=None)

    def __post_init__(self):
        self.ownerIdentity = OwnerIdentify.from_dict(self.ownerIdentity)


@dataclasses.dataclass
class Object(Base):
    key: T.Optional[str] = dataclasses.field(default=None)
    sequencer: T.Optional[str] = dataclasses.field(default=None)


@dataclasses.dataclass
class S3(Base):
    s3SchemaVersion: T.Optional[str] = dataclasses.field(default=None)
    configurationId: T.Optional[str] = dataclasses.field(default=None)
    bucket: T.Optional[Bucket] = dataclasses.field(default=None)
    object: T.Optional[Object] = dataclasses.field(default=None)

    def __post_init__(self):
        self.bucket = Bucket.from_dict(self.bucket)
        self.object = Object.from_dict(self.object)


@dataclasses.dataclass
class S3DeleteRecord(Base):
    eventVersion: T.Optional[str] = dataclasses.field(default=None)
    eventSource: T.Optional[str] = dataclasses.field(default=None)
    awsRegion: T.Optional[str] = dataclasses.field(default=None)
    eventTime: T.Optional[str] = dataclasses.field(default=None)
    eventName: T.Optional[str] = dataclasses.field(default=None)
    userIdentity: T.Optional[dict] = dataclasses.field(default=None)
    requestParameters: T.Optional[dict] = dataclasses.field(default=None)
    responseElements: T.Optional[dict] = dataclasses.field(default=None)
    s3: T.Optional[S3] = dataclasses.field(default=None)

    def __post_init__(self):
        self.s3 = S3.from_dict(self.s3)

    @property
    def event_datetime(self) -> datetime:
        return datetime.strptime(self.eventTime, "%Y-%m-%dT%H:%M:%S.%fZ")

    @property
    def bucket(self) -> str:
        return self.s3.bucket.name

    @property
    def key(self) -> str:
        return self.s3.object.key

    @property
    def uri(self) -> str:
        return f"s3://{self.bucket}/{self.key}"

    @property
    def arn(self) -> str:
        return f"arn:aws:s3:::{self.bucket}/{self.key}"


@dataclasses.dataclass
class S3DeleteEvent(Base):
    Records: T.List[S3DeleteRecord] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        self.Records = [S3DeleteRecord.from_dict(record) for record in self.Records]

    @classmethod
    def fake(
        cls,
        bucket: str = "example-bucket",
        key: str = "test/key",
    ) -> "S3DeleteEvent":
        return cls.from_dict(
            {
                "Records": [
                    {
                        "eventVersion": "2.0",
                        "eventSource": "aws:s3",
                        "awsRegion": "us-east-1",
                        "eventTime": "1970-01-01T00:00:00.000Z",
                        "eventName": "ObjectCreated:Put",
                        "userIdentity": {"principalId": "EXAMPLE"},
                        "requestParameters": {"sourceIPAddress": "127.0.0.1"},
                        "responseElements": {
                            "x-amz-request-id": "EXAMPLE123456789",
                            "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH",
                        },
                        "s3": {
                            "s3SchemaVersion": "1.0",
                            "configurationId": "testConfigRule",
                            "bucket": {
                                "name": bucket,
                                "ownerIdentity": {"principalId": "EXAMPLE"},
                                "arn": f"arn:aws:s3:::{bucket}",
                            },
                            "object": {
                                "key": key,
                                "sequencer": "0A1B2C3D4E5F678901",
                            },
                        },
                    }
                ]
            }
        )
