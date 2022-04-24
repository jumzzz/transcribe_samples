echo "Creating Bucket..."
aws s3 mb s3://transcribe-in-out-v2

echo "Putting Encryption..."
aws s3api put-bucket-encryption \
    --bucket transcribe-in-out-v2 \
    --server-side-encryption-configuration file://kms_config/s3_config.json

echo "Uploading ../input_video/"
aws s3 cp ../input_video/video.mp4 s3://transcribe-in-out-v2/input_video/video.mp4