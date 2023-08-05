# -*- coding: utf-8 -*-

import typing as T
import dataclasses
from datetime import datetime

from ..helpers import datetime_from_timestamp
from ..base import Base


@dataclasses.dataclass
class Dynamodb(Base):
    Keys: T.Dict[str, T.Dict[str, str]] = dataclasses.field(default_factory=dict)
    NewImage: T.Dict[str, T.Dict[str, str]] = dataclasses.field(default_factory=dict)
    OldImage: T.Dict[str, T.Dict[str, str]] = dataclasses.field(default_factory=dict)
    ApproximateCreationDateTime: T.Optional[int] = dataclasses.field(default=None)
    SequenceNumber: T.Optional[str] = dataclasses.field(default=None)
    SizeBytes: T.Optional[int] = dataclasses.field(default=None)
    StreamViewType: T.Optional[str] = dataclasses.field(default=None)

    @property
    def approximate_creation_datetime(self) -> datetime:
        return datetime_from_timestamp(self.ApproximateCreationDateTime)


@dataclasses.dataclass
class DynamodbUpdateRecord(Base):
    eventID: T.Optional[str] = dataclasses.field(default=None)
    eventName: T.Optional[str] = dataclasses.field(default=None)
    eventVersion: T.Optional[str] = dataclasses.field(default=None)
    eventSource: T.Optional[str] = dataclasses.field(default=None)
    awsRegion: T.Optional[str] = dataclasses.field(default=None)
    eventSourceARN: T.Optional[str] = dataclasses.field(default=None)
    dynamodb: T.Optional[Dynamodb] = dataclasses.field(default=None)

    def __post_init__(self):
        self.dynamodb = Dynamodb.from_dict(self.dynamodb)

    @property
    def is_insert(self) -> bool:
        return self.eventName == "INSERT"

    @property
    def is_update(self) -> bool:
        return self.eventName == "MODIFY"

    @property
    def is_delete(self) -> bool:
        return self.eventName == "REMOVE"

    @property
    def keys(self) -> T.Dict[str, T.Dict[str, str]]:
        return self.dynamodb.Keys

    @property
    def new_image(self) -> T.Dict[str, T.Dict[str, str]]:
        return self.dynamodb.NewImage

    @property
    def old_image(self) -> T.Dict[str, T.Dict[str, str]]:
        return self.dynamodb.OldImage

    @property
    def approximate_creation_timestamp(self) -> int:
        return self.dynamodb.ApproximateCreationDateTime

    @property
    def approximate_creation_datetime(self) -> datetime:
        return self.dynamodb.approximate_creation_datetime


@dataclasses.dataclass
class DynamodbUpdateEvent(Base):
    Records: T.List[DynamodbUpdateRecord] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        self.Records = [
            DynamodbUpdateRecord.from_dict(record) for record in self.Records
        ]

    @classmethod
    def fake(
        cls,
        keys: T.Optional[T.Dict[str, T.Dict[str, str]]] = None,
        new_image: T.Optional[T.Dict[str, T.Dict[str, str]]] = None,
        old_image: T.Optional[T.Dict[str, T.Dict[str, str]]] = None,
        approximate_creation_datetime: datetime = datetime(2000, 1, 1),
        sequence_number: str = "4421584500000000017450439091",
        is_insert: bool = False,
        is_update: bool = False,
        is_delete: bool = False,
    ) -> "DynamodbUpdateEvent":
        """
        :param new_image: will be used in insert and update
        :param old_image: will be used in update and delete
        """
        if sum([is_insert, is_update, is_delete]) != 1:
            raise ValueError(
                "one and only one 'is_insert', 'is_update', 'is_delete' can be True"
            )

        approximate_creation_timestamp = int(approximate_creation_datetime.timestamp())

        if is_insert:
            if keys is None:
                keys = {"Id": {"N": "101"}}
            if new_image is None:
                new_image = {"Message": {"S": "New item!"}, "Id": {"N": "101"}}
            record = {
                "eventID": "c4ca4238a0b923820dcc509a6f75849b",
                "eventName": "INSERT",
                "eventVersion": "1.1",
                "eventSource": "aws:dynamodb",
                "awsRegion": "us-east-1",
                "dynamodb": {
                    "Keys": keys,
                    "NewImage": new_image,
                    "ApproximateCreationDateTime": approximate_creation_timestamp,
                    "SequenceNumber": sequence_number,
                    "SizeBytes": 26,
                    "StreamViewType": "NEW_AND_OLD_IMAGES",
                },
                "eventSourceARN": "arn:aws:dynamodb:us-east-1:123456789012:table/ExampleTableWithStream/stream/2015-06-27T00:48:05.899",
            }
        elif is_update:
            if keys is None:
                keys = {"Id": {"N": "101"}}
            if new_image is None:
                new_image = {
                    "Message": {"S": "This item has changed"},
                    "Id": {"N": "101"},
                }
            if old_image is None:
                old_image = {"Message": {"S": "New item!"}, "Id": {"N": "101"}}
            record = {
                "eventID": "c81e728d9d4c2f636f067f89cc14862c",
                "eventName": "MODIFY",
                "eventVersion": "1.1",
                "eventSource": "aws:dynamodb",
                "awsRegion": "us-east-1",
                "dynamodb": {
                    "Keys": keys,
                    "NewImage": new_image,
                    "OldImage": old_image,
                    "ApproximateCreationDateTime": approximate_creation_timestamp,
                    "SequenceNumber": sequence_number,
                    "SizeBytes": 59,
                    "StreamViewType": "NEW_AND_OLD_IMAGES",
                },
                "eventSourceARN": "arn:aws:dynamodb:us-east-1:123456789012:table/ExampleTableWithStream/stream/2015-06-27T00:48:05.899",
            }
        elif is_delete:
            if keys is None:
                keys = {"Id": {"N": "101"}}
            if old_image is None:
                old_image = {
                    "Message": {"S": "This item has changed"},
                    "Id": {"N": "101"},
                }
            record = {
                "eventID": "eccbc87e4b5ce2fe28308fd9f2a7baf3",
                "eventName": "REMOVE",
                "eventVersion": "1.1",
                "eventSource": "aws:dynamodb",
                "awsRegion": "us-east-1",
                "dynamodb": {
                    "Keys": keys,
                    "OldImage": old_image,
                    "ApproximateCreationDateTime": approximate_creation_timestamp,
                    "SequenceNumber": sequence_number,
                    "SizeBytes": 38,
                    "StreamViewType": "NEW_AND_OLD_IMAGES",
                },
                "eventSourceARN": "arn:aws:dynamodb:us-east-1:123456789012:table/ExampleTableWithStream/stream/2015-06-27T00:48:05.899",
            }
        else:  # pragma: no cover
            raise
        data = {"Records": [record]}
        return cls.from_dict(data)
