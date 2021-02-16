import boto3
from botocore.exceptions import ClientError

TABLE_NAME = 'request'

class Model():
    def __init__(self):
        self.resource = boto3.resource("dynamodb")
        self.table = self.resource.Table(TABLE_NAME)
        try:
            self.table.load() # check if table exists
        except:
            self.resource.create_table(
                TableName=TABLE_NAME,
                KeySchema=[
                    {
                        "AttributeName": "request_id",
                        "KeyType": "HASH"
                    }
                ],
                AttributeDefinitions=[
                    {
                        "AttributeName": "request_id",
                        "AttributeType": "N"
                    },
                    {
                        "AttributeName": "status",
                        "AttributeType": "S"
                    }
                ],
                ProvisionedThroughput={
                    "ReadCapacityUnits": 10,
                    "WriteCapacityUnits": 10
                }
            )
    
    
    def get_request(self, id):
        try:
            response = self.table.get_item(Key={'request_id': id})
        except ClientError as e:
            # Handle exception
            return True, e.response['Error']['Message']

        return False, response['Item']

    def update_request(self, id, status):
        # no try except blocks because this update isn't critical and won't result in different return values
        self.table.update_item(
            Key={
                'request_id': id   
            },
            UpdateExpression="set status=:s",
            ExpressionAttributeValues={
                ':s': status
            }
        )

    def post_request(self, id, status):
        try:
            self.table.put_item(Item={'request_id': id, 'status': status})
        except ClientError as e:
            # Not sure how to handle this exception
            return False
        
        return True
