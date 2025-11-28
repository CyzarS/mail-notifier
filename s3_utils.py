import os
from datetime import datetime
import boto3

_s3 = boto3.client("s3")
BUCKET = os.getenv("S3_BUCKET")

def head_metadata(key):
    if not BUCKET:
        raise RuntimeError("S3_BUCKET no configurado")
    resp = _s3.head_object(Bucket=BUCKET, Key=key)
    return resp.get("Metadata", {})

def update_metadata(key, metadata):
    if not BUCKET:
        raise RuntimeError("S3_BUCKET no configurado")
    _s3.copy_object(
        Bucket=BUCKET,
        Key=key,
        CopySource={"Bucket": BUCKET, "Key": key},
        Metadata=metadata,
        MetadataDirective="REPLACE",
        ContentType="application/pdf",
    )
