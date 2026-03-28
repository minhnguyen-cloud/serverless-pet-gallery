import boto3
import os

# Initialize the DynamoDB resource
# (Khởi tạo kết nối với dịch vụ DynamoDB)
dynamodb = boto3.resource('dynamodb')

# Define the table name from Environment Variables 
# Get the table name
table_name = os.environ.get('TABLE_NAME', 'PetImageViews')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    """
    This function is triggered by EventBridge when an image is accessed via S3 GetObject.
    It increments the view count in DynamoDB.
    """
    try:
        # Extract the image file name (object key) from the event payload
        # (Extracting image filenames from event data packets)
        detail = event.get('detail', {})
        request_parameters = detail.get('requestParameters', {})
        image_id = request_parameters.get('key')

        if not image_id:
            print("No image key found in the event.")
            return {'statusCode': 400, 'body': 'Image ID not found'}

        # Update the database using DynamoDB Atomic Counters
        # (Using DynamoDB's Atomic Counter feature for safe accumulation)
        response = table.update_item(
            Key={
                'ImageID': image_id
            },
            UpdateExpression="ADD ViewCount :inc",
            ExpressionAttributeValues={
                ':inc': 1
            },
            ReturnValues="UPDATED_NEW"
        )

        # Log the success message
        new_count = response['Attributes'].get('ViewCount', 1)
        print(f"Successfully updated! Image: {image_id} | New View Count: {new_count}")

        return {
            'statusCode': 200,
            'body': f'Success. Current count: {new_count}'
        }

    except Exception as e:
        print(f"Error processing the event: {str(e)}")
        return {'statusCode': 500, 'body': 'Internal server error'}
