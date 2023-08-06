import os
import tempfile
import boto3


def download_resource(bucket: str, path: str) -> str:
    dst = os.path.join("/tmp", "pypolar", path)
    if os.path.exists(dst):
        return dst

    os.makedirs(os.path.dirname(dst), exist_ok=True)
    boto3.client('s3').download_file(bucket, path, dst)
    return dst
