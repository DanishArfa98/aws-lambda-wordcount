import json
import urllib.parse
import boto3

s3 = boto3.client('s3')
sns = boto3.client('sns')

SNS_TOPIC_ARN = 'arn:aws:sns:us-west-2:321188625619:WordCountTopic'

def lambda_handler(event, context):
    try:
        # 1. Ambil nama bucket dan nama file (key) dari event S3 Trigger
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

        # 2. Unduh konten file dari S3
        response = s3.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read().decode('utf-8')

        # 3. Hitung jumlah kata
        words = content.split()
        word_count = len(words)

        # 4. Format pesan dan subjek sesuai ketentuan lab
        message = f"The word count in the {key} file is {word_count}."
        subject = "Word Count Result"

        # 5. Kirim pesan ke SNS Topic
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject=subject
        )

        return {
            'statusCode': 200,
            'body': json.dumps(f'Success! Processed {key} with {word_count} words.')
        }

    except Exception as e:
        print(f"Error processing object {key} from bucket {bucket}: {e}")
        raise e