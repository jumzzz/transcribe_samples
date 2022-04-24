aws s3 mb s3://transcribe-in-out

aws s3api put-bucket-encryption \
    --bucket transcribe-in-out \
    --server-side-encryption-configuration file://kms_config/s3_config.json