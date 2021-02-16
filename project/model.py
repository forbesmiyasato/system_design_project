import boto3
import time
from decimal import Decimal
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
                        "AttributeType": "S"
                    }
                ],
                ProvisionedThroughput={
                    "ReadCapacityUnits": 10,
                    "WriteCapacityUnits": 10
                }
            )
        time.sleep(5) # give table some to be created for the subsequent post request


    def get_request(self, id):
        try:
            response = self.table.get_item(Key={'request_id': id})
        except ClientError as e:
            # Handle exception
            return True, e.response['Error']['Message']

        if 'Item' not in response:
            return True, f"{id} doesn't exist"

        return False, response['Item']

    def update_request(self, id, status, status_code):
        # no try except blocks because this update isn't critical and won't result in different return values
        self.table.update_item(
            Key={
                'request_id': id
            },
            UpdateExpression="SET request_status=:s, code=:c",
            ExpressionAttributeValues={
                ':s': status,
                ':c': Decimal(int(status_code))
            }
        )

    def post_request(self, id, status, code):
        try:
            self.table.put_item(Item={'request_id': id, 'request_status': status, 'code': code})
        except ClientError as e:
            # Not sure how to handle this exception
            print(e.response['Error']['Message'])
            return False
        
        return True
