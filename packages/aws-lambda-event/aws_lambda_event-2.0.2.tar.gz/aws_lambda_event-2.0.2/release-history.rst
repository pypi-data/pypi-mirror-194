.. _release_history:

Release and Version History
==============================================================================


Backlog
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


2.0.2 (2023-02-25)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Bugfixes**

- add ``version`` field to ``CloudWatchScheduledEvent`` event object.

**Miscellaneous**

- update README


2.0.1 (2023-02-04)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Breaking Changes**

- use ``dataclasses`` everywhere. The original initialization method ``Event(data: dict)`` no longer work. Now it use ``Event.from_dict(data: dict)`` for initialization.

**Features and Improvements**

- add ``CloudWatchLogsEvent`` event object.
- add ``CloudWatchScheduledEvent`` event object.


1.0.1 (2022-01-16)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``S3PutEvent`` event object.
- add ``S3DeleteEvent`` event object.
- add ``SNSTopicNotificationEvent`` event object.
- add ``SQSEvent`` event object.
- add ``DynamodbUpdateEvent`` event object.
- add ``KinesisStreamEvent`` event object.
- add ``KinesisFirehoseEvent`` event object.

**Miscellaneous**

- ``aws_lambda_event`` library 1.X.X aim to zero dependencies.
