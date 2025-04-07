# AWS Lambda Image Resizer

This AWS Lambda function automatically resizes images uploaded to an S3 bucket and saves the resized versions to another S3 bucket.

## Overview

When an image is uploaded to the source S3 bucket, the Lambda function is triggered, downloads the image, resizes it to 300x300 pixels, and uploads the resized version to the target S3 bucket.

## Prerequisites

- AWS account with appropriate permissions
- Two S3 buckets:
  - Source bucket: Where original images are uploaded
  - Target bucket: Where resized images are stored

## Deployment Instructions

### 1. Set Up Dependencies

When deploying to AWS Lambda, you need to include the Pillow library with the correct binaries. Use one of these approaches:

#### Option 1: Install dependencies for Lambda environment

```bash
pip install pillow --platform manylinux2014_x86_64 --target ./package --implementation cp --python-version 3.9 --only-binary=:all: --upgrade
```

#### Option 2: Use Docker to build the package

```bash
docker run -v "$PWD":/var/task "public.ecr.aws/sam/build-python3.9" /bin/sh -c "pip install pillow -t /var/task"
```

### 2. Create Deployment Package

```bash
# If using --target ./package approach
cd package
zip -r ../deployment_package.zip .
cd ..
zip deployment_package.zip lambda_function.py

# If using Docker approach, zip from the current directory
zip -r deployment_package.zip .
```

### 3. Configure AWS Lambda

1. Create a new Lambda function in the AWS Console
2. Upload the deployment package
3. Set the handler to `lambda_function.lambda_handler`
4. Configure an S3 trigger for your source bucket
5. Set an appropriate timeout (recommend at least 10 seconds)
6. Configure environment variables if needed

### 4. Set IAM Permissions

Ensure your Lambda execution role has the following permissions:

- `s3:GetObject` on the source bucket
- `s3:PutObject` on the target bucket

Example IAM policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::SOURCE-BUCKET-NAME/*"
    },
    {
      "Effect": "Allow",
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::TARGET-BUCKET-NAME/*"
    }
  ]
}
```

Replace `SOURCE-BUCKET-NAME` and `TARGET-BUCKET-NAME` with your actual bucket names.

## Common Issues & Troubleshooting

1. **PIL/Pillow Import Error**: Ensure you're installing Pillow with the correct binaries for Amazon Linux.

2. **Bucket Not Found**: Verify that both source and target buckets exist and are spelled correctly.

3. **Permission Issues**: Check that your Lambda execution role has the necessary S3 permissions.

4. **Timeout Errors**: For larger images, you may need to increase the Lambda timeout.

## Customization

- Adjust the `new_size` variable to change the dimensions of the resized images
- Modify the image format by changing the `format` parameter in the `save` method
- Add watermarking or other image processing by extending the `process_image` function
