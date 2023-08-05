# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from ..base import Base


@dataclasses.dataclass
class SQSRecord(Base):
    messageId: T.Optional[str] = dataclasses.field(default=None)
    receiptHandle: T.Optional[str] = dataclasses.field(default=None)
    body: T.Optional[str] = dataclasses.field(default=None)
    attributes: dict = dataclasses.field(default_factory=dict)
    messageAttributes: dict = dataclasses.field(default_factory=dict)
    md5OfBody: T.Optional[str] = dataclasses.field(default=None)
    eventSource: T.Optional[str] = dataclasses.field(default=None)
    eventSourceARN: T.Optional[str] = dataclasses.field(default=None)
    awsRegion: T.Optional[str] = dataclasses.field(default=None)


@dataclasses.dataclass
class SQSEvent(Base):
    Records: T.List[SQSRecord] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        self.Records = [SQSRecord.from_dict(record) for record in self.Records]

    @classmethod
    def fake(
        cls,
        message_id: str = "19dd0b57-b21e-4ac1-bd88-01bbb068cb78",
        receipt_handler: str = "MessageReceiptHandle",
        body: str = "Hello from SQS!",
        message_attribute: T.Optional[dict] = None,
    ) -> "SQSEvent":
        if message_attribute is None:
            message_attribute = {}
        data = {
            "Records": [
                {
                    "messageId": message_id,
                    "receiptHandle": receipt_handler,
                    "body": body,
                    "attributes": {
                        "ApproximateReceiveCount": "1",
                        "SentTimestamp": "1523232000000",
                        "SenderId": "123456789012",
                        "ApproximateFirstReceiveTimestamp": "1523232000001",
                    },
                    "messageAttributes": message_attribute,
                    "md5OfBody": "{{{md5_of_body}}}",
                    "eventSource": "aws:sqs",
                    "eventSourceARN": "arn:aws:sqs:us-east-1:123456789012:MyQueue",
                    "awsRegion": "us-east-1",
                }
            ]
        }
        return cls.from_dict(data)
