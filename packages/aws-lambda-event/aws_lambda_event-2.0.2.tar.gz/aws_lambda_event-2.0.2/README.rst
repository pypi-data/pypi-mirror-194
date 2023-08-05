.. image:: https://github.com/MacHu-GWU/aws_lambda_event-project/workflows/CI/badge.svg
    :target: https://github.com/MacHu-GWU/aws_lambda_event-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/aws_lambda_event-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/aws_lambda_event-project

.. image:: https://img.shields.io/pypi/v/aws_lambda_event.svg
    :target: https://pypi.python.org/pypi/aws_lambda_event

.. image:: https://img.shields.io/pypi/l/aws_lambda_event.svg
    :target: https://pypi.python.org/pypi/aws_lambda_event

.. image:: https://img.shields.io/pypi/pyversions/aws_lambda_event.svg
    :target: https://pypi.python.org/pypi/aws_lambda_event

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/aws_lambda_event-project

------

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/aws_lambda_event-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/aws_lambda_event-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/aws_lambda_event-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/aws_lambda_event#files


Welcome to ``aws_lambda_event`` Documentation
==============================================================================
This library provides Python Class interface, attribute auto-complete, type hint for AWS Lambda Events. It can parse the AWS Lambda event data, and also generate fake event data for testing.

**Example**:

.. code-block:: python

    # An example lambda handler python module
    import aws_lambda_event

    # parse S3 Put event, convert it into a python object with type hint, auto complete
    def handler(event, context):
        event_obj = aws_lambda_event.S3PutEvent.from_dict(event)

        for record in event_obj.Records:
            # access attribute
            _ = record.eventTime

            # important attributes quick access alias
            _ = record.bucket
            _ = record.key
            _ = record.etag
            _ = record.size
            ...

    # generate an fake event for testing
    event_obj = aws_lambda_event.S3PutEvent.fake(bucket="my-bucket", key="my-file.txt")
    ...


**List of Supported Event**:

- ``CloudWatchLogsEvent``
- ``CloudWatchScheduledEvent``
- ``S3PutEvent``
- ``S3DeleteEvent``
- ``SNSTopicNotificationEvent``
- ``SQSEvent``
- ``DynamodbUpdateEvent``
- ``KinesisStreamEvent``
- ``KinesisFirehoseEvent``

You can find the event JSON schema in two place:

1. AWS Lambda Event Source Mapping Official Document: https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventsourcemapping.html
2. Goto AWS Lambda Function Console -> Create Test Event -> Choose from Event template


.. _install:

Install
------------------------------------------------------------------------------

``aws_lambda_event`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install aws_lambda_event

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade aws_lambda_event