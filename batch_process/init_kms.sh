mkdir -p kms_config
aws kms create-key \
    --tags TagKey=Purpose,TagValue=Test \
    --description "Development Test Key" > kms_config/kms_config.json

python parse_s3_kms.py kms_config/kms_config.json kms_config/s3_config.json
