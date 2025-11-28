import os
import boto3

_ses = boto3.client("ses", region_name=os.getenv("AWS_REGION", "us-east-1"))
FROM_ADDR = os.getenv("SES_FROM")

def send_note_email(to_email, subject, html_body):
    if not FROM_ADDR:
        raise RuntimeError("SES_FROM no configurado")
    _ses.send_email(
        Source=FROM_ADDR,
        Destination={"ToAddresses": [to_email]},
        Message={
            "Subject": {"Data": subject, "Charset": "UTF-8"},
            "Body": {"Html": {"Data": html_body, "Charset": "UTF-8"}},
        },
    )
