from PIL import Image
from io import BytesIO
import boto3
import logging

#Initialize the s3 client
s3_client = boto3.client('s3')

# Initialize the logger
logger = logging.getLogger()
logger.setLevel("INFO")

def download_image_from_s3(bucket_name, key):
    try:
        # Download the image from s3
        response = s3_client.get_object(Bucket=bucket_name, Key=key)
        img_data = response['Body'].read() # Read the image data

        # Convert image data to a bytesIO object
        img = Image.open(BytesIO(img_data))
        return img
    except Exception as e:
        logger.error(f"Error downoading image: {str(e)}")
        return None
def upload_image_to_s3(bucket_name, key, img):
    try:
        # Save the image to a BytesIO object
        img_byte_array = BytesIO()
        img.save(img_byte_array, format='JPEG')
        img_byte_array.seek(0)

        # Upload the image back to s3
        s3_client.put_object(Bucket=bucket_name, Key=key, Body=img_byte_array)
        print(f"Image uploaded successfully to {bucket_name}/{key}")
    except Exception as e:
        logger.error(f"Error uploading image: {str(e)}")
        raise

def resize_image(img, size):
    return img.resize(size)

def process_image(source_bucket_name, target_bucket_name, source_key, target_key, new_size):

    # Download the image from s3
    img = download_image_from_s3(source_bucket_name, source_key)

    if img:
        # Resize the image
        resized_img = resize_image(img, new_size)

        # Upload the resized iamge back to s3
        upload_image_to_s3(target_bucket_name, target_key, resized_img)

def lambda_handler(event, context):
    try:
        # set source
        source_bucket = event['Records'][0]['s3']['bucket']['name']
        source_key = event['Records'][0]['s3']['object']['key']

        # set target
        target_bucket = "mitch-rs-images"
        target_key = f"resized{source_key}"
        new_size = (300, 300)

        # Resize image
        process_image(source_bucket, target_bucket, source_key, target_key, new_size)
        
        return {
            "statusCode": 200,
            "message": "Image resized successfully"
        }

    except Exception as e:
        logger.error(f"Error resizing image: {str(e)}")
        raise
