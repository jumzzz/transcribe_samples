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