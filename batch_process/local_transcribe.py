import boto3
import argparse
import time
import json


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bucket', help='Bucket name.')
    parser.add_argument('--input_key', help='Key result.')
    parser.add_argument('--output_key', help='Output key.')
    parser.add_argument('--job_name', help='Transcription Job Name.')
    parser.add_argument('--s3_kms_config', help='KMS Config of your S3.')

    args = parser.parse_args()
    return args


def get_kms_key_id(s3_kms_path):
    with open(s3_kms_path, 'r') as f:
        kms_config = json.load(f)
        return kms_config['KeyMetadata']['KeyId']


def transcribe_mp4(s3_bucket, input_key, output_key, kms_key_id, job_name):

    client = boto3.client('transcribe')

    session = boto3.session.Session()
    region = session.region_name

    media_input = {
     #   'MediaFileUri': f's3://s3-{region}.amazonaws.com/{s3_bucket}/{input_key}'
        'MediaFileUri': f's3://{s3_bucket}/{input_key}'
    }

    subtitles = {
        'Formats': [
           'srt'
        ],
        'OutputStartIndex': 1
    }

    print('Initializing client.start_transcription_job(...)')
    print(f'job_name = {job_name}')
    print(f'media_input = {media_input}')
    print(f'subtitles = {subtitles}')
    print(f'kms_key_id = {kms_key_id}')
    print(f's3_bucket = {s3_bucket}')
    print(f'output_key = {output_key}')

    client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media=media_input,
            Subtitles=subtitles,
            OutputEncryptionKMSKeyId=kms_key_id,
            OutputBucketName=s3_bucket,
            OutputKey=output_key,
            LanguageCode='en-IE',
            MediaFormat='mp4'
    )

    status = client.get_transcription_job(TranscriptionJobName=job_name)

    while status['TranscriptionJob']['TranscriptionJobStatus'].lower() != 'completed':
        print('Status Check - Not yet completed...')
        time.sleep(5)
        status = client.get_transcription_job(TranscriptionJobName=job_name)


def try_transcribe_mp4(s3_bucket, input_key, output_key, kms_key_id, job_name):
    try:
        transcribe_mp4(s3_bucket, input_key, output_key, kms_key_id, job_name)
    except Exception as e:
        print(e)
        

def main():
    args = get_args()

    s3_bucket = args.bucket
    input_key = args.input_key
    output_key = args.output_key
    job_name = args.job_name
    s3_kms_config = args.s3_kms_config
    kms_key_id = get_kms_key_id(s3_kms_config)

    print(f's3_bucket = {s3_bucket}')
    print(f'input_key = {input_key}')
    print(f'output_key = {output_key}')
    print(f'job_name = {job_name}')
    print(f's3_kms_config = {s3_kms_config}')
    print(f'kms_key_id = {kms_key_id}')

    transcribe_mp4(s3_bucket, input_key, output_key, kms_key_id,job_name)


if __name__ == '__main__':
    main()
