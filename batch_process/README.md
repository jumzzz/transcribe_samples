# Stream Processing with AWS Transcribe

## TODO
1. Create an SSE-KMS Key for Encryption at Rest to S3
2. Create an S3 bucket that uses the created SSE-KMS Key for encryption
3. Create a Python Script that Dumps Audio Files to S3
4. Create an Event Trigger for Lambda that does the following
   - Consume an Audio File with Retries
   - Move the File on another S3 Bucket/Key after consumption
   - Send the results to S3

5. Download the Transcription and commit the results


### Step 1: Creating a Custom Managed Key

Creation of SSE-KMS managed key is implemented on `init_kms.sh`

Basically the important AWS CLI command here is:

```
aws kms create-key \
    --tags TagKey=Purpose,TagValue=Test \
    --description "Development Test Key" > kms_config/kms_config.json

```

Which produces an output of:
```
{
    "KeyMetadata": {
        "AWSAccountId": "451713003466",
        "KeyId": "00000000-0000-0000-0000-000000000000",
        "Arn": "arn:aws:kms:us-east-1:451713003466:key/00000000-0000-0000-0000-000000000000",
        "CreationDate": "2022-04-24T16:58:06.053000+08:00",
        "Enabled": true,
        "Description": "Development Test Key",
        "KeyUsage": "ENCRYPT_DECRYPT",
        "KeyState": "Enabled",
        "Origin": "AWS_KMS",
        "KeyManager": "CUSTOMER",
        "CustomerMasterKeySpec": "SYMMETRIC_DEFAULT",
        "KeySpec": "SYMMETRIC_DEFAULT",
        "EncryptionAlgorithms": [
            "SYMMETRIC_DEFAULT"
        ],
        "MultiRegion": false
    }
}

```
I also made a parser of `KMSMasterKeyID` on `parse_s3_kms.py` which generates a json of

```
{
    "Rules": [
        {
            "ApplyServerSideEncryptionByDefault": {
                "SSEAlgorithm": "aws:kms",
                "KMSMasterKeyID": "ee9466c8-5671-4da0-9dbc-93c1e4e8538d"
            },
            "BucketKeyEnabled": false
        }
    ]
}
```

### Step 2: Creating an S3 Bucket with SSE-KMS Encryption enabled

First let's create a bucket transcribe-in-out:

```
aws s3 mb s3://transcribe-in-out
```

Then let's dump the object `../input_video/video.mp4`

```
aws s3 cp ../input_video/video.mp4 s3://transcribe-in-out/input_video/video.mp4
```

Then let's add an encryption

```
aws s3api put-bucket-encryption \
    --bucket transcribe-in-out \
    --server-side-encryption-configuration file://kms_config/s3_config.json
```

We can verify if the object inside is also encrypted using 
```
aws s3api get-object --bucket transcribe-in-out --key input_video/video.mp4 out.mp4
```
Which results to output, notice that there's a key for `ServerSideEncryption`

```
{
    "AcceptRanges": "bytes",
    "LastModified": "2022-04-24T09:56:43+00:00",
    "ContentLength": 9901473,
    "ETag": "\"7b3fa90fcc99996ba7415c1304baa4a1-2\"",
    "ContentType": "video/mp4",
    "ServerSideEncryption": "aws:kms",
    "Metadata": {},
    "SSEKMSKeyId": "arn:aws:kms:us-east-1:451713003466:key/00000000-0000-0000-0000-000000000000"
}
```
