# -*- coding: utf-8 -*-

"""
Class Interface for AWS Lambda event.
"""

from ._version import __version__

__short_description__ = "Class Interface for AWS Lambda event."
__license__ = "MIT"
__author__ = "Sanhe Hu"
__author_email__ = "husanhe@gmail.com"
__github_username__ = "MacHu-GWU"

try:
    from .events.cloudwatch_logs import CloudWatchLogsEvent
    from .events.cloudwatch_scheduled_event import CloudWatchScheduledEvent
    from .events.s3_put import S3PutEvent
    from .events.s3_delete import S3DeleteEvent
    from .events.sns import SNSTopicNotificationEvent
    from .events.sqs import SQSEvent
    from .events.dynamodb_update import DynamodbUpdateEvent
    from .events.kinesis_stream import KinesisStreamEvent
    from .events.kinesis_firehose import KinesisFirehoseEvent
except ImportError:  # pragma: no cover
    pass
except:  # pragma: no cover
    raise
