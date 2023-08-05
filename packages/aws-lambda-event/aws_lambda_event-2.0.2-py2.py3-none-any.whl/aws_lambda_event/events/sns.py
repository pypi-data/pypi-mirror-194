# -*- coding: utf-8 -*-

import typing as T
import dataclasses
from datetime import datetime

from ..base import Base


@dataclasses.dataclass
class SNS(Base):
    Type: T.Optional[str] = dataclasses.field(default=None)
    MessageId: T.Optional[str] = dataclasses.field(default=None)
    TopicArn: T.Optional[str] = dataclasses.field(default=None)
    Subject: T.Optional[str] = dataclasses.field(default=None)
    Message: T.Optional[str] = dataclasses.field(default=None)
    Timestamp: T.Optional[str] = dataclasses.field(default=None)
    SignatureVersion: T.Optional[str] = dataclasses.field(default=None)
    Signature: T.Optional[str] = dataclasses.field(default=None)
    SigningCertUrl: T.Optional[str] = dataclasses.field(default=None)
    UnsubscribeUrl: T.Optional[str] = dataclasses.field(default=None)
    MessageAttributes: T.Optional[dict] = dataclasses.field(default=None)

    @property
    def notification_time(self) -> datetime:
        return datetime.strptime(self.Timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")


@dataclasses.dataclass
class SNSRecord(Base):
    EventSource: T.Optional[str] = dataclasses.field(default=None)
    EventVersion: T.Optional[str] = dataclasses.field(default=None)
    EventSubscriptionArn: T.Optional[str] = dataclasses.field(default=None)
    Sns: T.Optional[SNS] = dataclasses.field(default=None)

    def __post_init__(self):
        self.Sns = SNS.from_dict(self.Sns)

    @property
    def message(self) -> str:
        return self.Sns.Message

    @property
    def subject(self) -> str:
        return self.Sns.Subject

    @property
    def notification_time(self) -> datetime:
        return self.Sns.notification_time


@dataclasses.dataclass
class SNSTopicNotificationEvent(Base):
    Records: T.List[SNSRecord] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        self.Records = [SNSRecord.from_dict(record) for record in self.Records]

    @classmethod
    def fake(
        cls,
        subject: str = "example subject",
        message: str = "example message",
        message_attribute: T.Optional[dict] = None,
        notification_time: datetime = datetime(2000, 1, 1),
    ) -> "SNSTopicNotificationEvent":
        if message_attribute is None:
            message_attribute = {
                "Test": {"Type": "String", "Value": "TestString"},
                "TestBinary": {"Type": "Binary", "Value": "TestBinary"},
            }
        data = {
            "Records": [
                {
                    "EventSource": "aws:sns",
                    "EventVersion": "1.0",
                    "EventSubscriptionArn": "arn:aws:sns:us-east-1:123456789012:ExampleTopic",
                    "Sns": {
                        "Type": "Notification",
                        "MessageId": "95df01b4-ee98-5cb9-9903-4c221d41eb5e",
                        "TopicArn": "arn:aws:sns:us-east-1:123456789012:ExampleTopic",
                        "Subject": subject,
                        "Message": message,
                        "Timestamp": notification_time.strftime(
                            "%Y-%m-%dT%H:%M:%S.%fZ"
                        ),
                        "SignatureVersion": "1",
                        "Signature": "EXAMPLE",
                        "SigningCertUrl": "EXAMPLE",
                        "UnsubscribeUrl": "EXAMPLE",
                        "MessageAttributes": message_attribute,
                    },
                }
            ]
        }
        return cls.from_dict(data)
