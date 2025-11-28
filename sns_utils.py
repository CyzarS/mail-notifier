import os
import boto3

_sns = boto3.client("sns", region_name=os.getenv("AWS_REGION", "us-east-1"))
TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")

def send_sns_notification(subject, message):
    if not TOPIC_ARN:
        print("SNS_TOPIC_ARN no configurado, omitiendo envío SNS")
        return

    try:
        _sns.publish(
            TopicArn=TOPIC_ARN,
            Subject=subject[:100],  # SNS subject limit
            Message=message
        )
        print(f"Notificación SNS enviada a {TOPIC_ARN}")
    except Exception as e:
        print(f"Error enviando SNS: {e}")
