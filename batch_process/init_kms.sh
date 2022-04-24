mkdir -p kms_config
aws kms create-key \
    --tags TagKey=Purpose,TagValue=Test \
    --description "Development Test Key" > kms_config/kms_config.json
