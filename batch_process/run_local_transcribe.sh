python local_transcribe.py --bucket transcribe-in-out-v2 \
                    --input_key input_video/video.mp4 \
                    --output_key output_result/transcribe_data \
                    --job_name transcription-mp4-job \
                    --s3_kms_config kms_config/kms_config.json
