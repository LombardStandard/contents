import json
import boto3
import base64

S3_CLIENT = boto3.client('s3')
BUCKET_NAME = 'lombardst'


def api(event, context):

    DATA = json.loads(event['body'])
    IMAGE_DATA = base64.b64decode(DATA['img'].split(',')[1])
    FILE_NAME = 'cities/' + DATA['name'].replace(' ', '') + '.jpg'

    S3_CLIENT.put_object(
        Body=IMAGE_DATA,
        Bucket=BUCKET_NAME,
        Key=FILE_NAME,
        ACL='authenticated-read',
        ContentType='image/jpeg'
    )

    url = S3_CLIENT.generate_presigned_url(
        'get_object',
        Params={'Bucket': BUCKET_NAME, 'Key': FILE_NAME},
    )

    response = {
        "statusCode": 200,
        "headers": {'Access-Control-Allow-Origin': '*'},
        "body": url.split('?')[0]
    }

    return response
