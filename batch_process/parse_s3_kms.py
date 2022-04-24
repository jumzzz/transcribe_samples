import argparse
import json

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('src', help='Source input of generated kms_config.json')
    parser.add_argument('dst', help='Destination Path of s3_kms.json')

    args = parser.parse_args()
    return args

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def dump_json(path, data):
    with open(path, 'w') as f:
        data_str = json.dumps(data, indent=4)
        print(f'Dumping s3_config = {data_str}')
        f.write(data_str)

def main():
    args = get_args()
    src_config = load_json(args.src)
    kms_key_id = src_config['KeyMetadata']['KeyId']

    dst_config = {
        'Rules': [
            {
                'ApplyServerSideEncryptionByDefault': {
                    "SSEAlgorithm": 'aws:kms',
                    'KMSMasterKeyID': kms_key_id
                },
            'BucketKeyEnabled': False
            }
        ]
    }

    dump_json(args.dst, dst_config)
    

if __name__ == '__main__':
    main()