from boto3 import client
import json
from os import environ

from math import ceil

AWS_SQS_BATCH_LIMIT = 10


def set_aws_profile_region(region: str, profile: str):
    """
    Tells AWS which profile and region to use for the rest of this application by setting the corresponding environment variables and possibly overriding them if they were previously configured
    """

    environ["AWS_PROFILE"] = profile
    environ["AWS_DEFAULT_REGION"] = region


def get_queue_link(queue_name: str) -> str:
    """
    Gets the Queue Link from its name. (Required to push/pull items on the SQS)
    """

    awsClient = client("sqs")

    # Get SQS queue link
    response = awsClient.get_queue_url(QueueName=queue_name)

    return response["QueueUrl"]


def push_message_to_queue(queue_name: str, queue_messages: list) -> dict:
    """
    Converts a list of messages into an aws compliant structure to send messages into SQS and pushes them in batches of 10 the queue specified by its name
    """

    queue_link = get_queue_link(queue_name)

    awsClient = client("sqs")

    # Prepare AWS messages
    aws_messages_batch = [
        {
            "Id": str(queue_messages.index(single_message)),
            "MessageBody": json.dumps(single_message),
            "DelaySeconds": 1,
        }
        for single_message in queue_messages
    ]

    # Send messages in batches of AWS_SQS_BATCH_LIMIT (Currently the maximum available is 10)
    result = {}
    while aws_messages_batch:
        batch_items = aws_messages_batch[:AWS_SQS_BATCH_LIMIT]
        del aws_messages_batch[:AWS_SQS_BATCH_LIMIT]

        batch_results = awsClient.send_message_batch(
            QueueUrl=queue_link, Entries=batch_items
        )

        result.update(batch_results)

    return result


def get_message_from_queue(queue_name: str, max_messages: int = 10) -> list:
    """
    From a queue name, get up to the specified number of messages requested, returning their body and ID information (The ID is important to delete the message later on!)
    """
    message_list = []

    queue_link = get_queue_link(queue_name)
    awsClient = client("sqs")

    request_total = ceil(max_messages / AWS_SQS_BATCH_LIMIT)
    messages_to_read = (
        AWS_SQS_BATCH_LIMIT if max_messages > AWS_SQS_BATCH_LIMIT else max_messages
    )

    for _ in range(request_total):
        context_messages = awsClient.receive_message(
            QueueUrl=queue_link, MaxNumberOfMessages=messages_to_read, WaitTimeSeconds=1
        )

        # If there are no more messages to be read, we are done here.
        if not ("Messages" in context_messages):
            break

        # Read objects with queue data
        for message in context_messages["Messages"]:
            message_list.append(
                {"body": message["Body"], "id": message["ReceiptHandle"]}
            )

    return message_list


def delete_mesasge_from_queue(queue_name: str, messages_id: list) -> bool:
    """
    Deletes a set of messages from SQS, where the messages to be deleted are specified by its ID
    """

    queue_link = get_queue_link(queue_name)
    awsClient = client("sqs")

    messages_to_process = messages_id.copy()

    while messages_to_process:
        batch_items = messages_to_process[:AWS_SQS_BATCH_LIMIT]
        del messages_to_process[:AWS_SQS_BATCH_LIMIT]

        messages_to_be_removed = [
            {
                "Id": str(messages_id.index(single_message_id)),
                "ReceiptHandle": single_message_id,
            }
            for single_message_id in batch_items
        ]
        awsClient.delete_message_batch(
            QueueUrl=queue_link, Entries=messages_to_be_removed
        )

    return True
