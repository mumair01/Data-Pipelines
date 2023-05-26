# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-05-23 13:10:50
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-05-23 13:31:45

import boto3


def download_from_aws():
    s3 = boto3.client("s3")
    s3.download_file(
        Bucket="datapipelinesdatasets",
        Key="gailbot_receipts",
        Filename="data_downloaded",
    )


if __name__ == "__main__":
    # Let's use Amazon S3
    s3 = boto3.resource(
        "s3",
    )

    # Print out bucket names
    for bucket in s3.buckets.all():
        print(bucket.name)
