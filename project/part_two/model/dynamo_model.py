import boto3
import time
from .model import Model
from botocore.exceptions import ClientError


class DynamoDB(Model):
    def __init__(self):
        """
        Initializes the class. Creates DynamoDB Table if table doesn't exist.
        """
        self.resource = boto3.resource("dynamodb")
        self.table = self.resource.Table(self.TABLE_NAME)
        try:
            self.table.load()  # check if table exists
        except Exception:
            self.resource.create_table(
                TableName=self.TABLE_NAME,
                KeySchema=[{"AttributeName": "request_id", "KeyType": "HASH"}],
                AttributeDefinitions=[
                    {"AttributeName": "request_id", "AttributeType": "S"}
                ],
                ProvisionedThroughput={
                    "ReadCapacityUnits": 10,
                    "WriteCapacityUnits": 10,
                },
            )
        # give table some time to be created for the subsequent post request
        time.sleep(5)

    def get_request(self, id):
        try:
            response = self.table.get_item(Key={"request_id": id})
        except ClientError as e:
            # Handle exception
            return True, e.response["Error"]["Message"]

        if "Item" not in response:
            return True, f"{id} doesn't exist"

        return False, response["Item"]

    def update_request(self, id, status, status_code):
        self.table.update_item(
            Key={"request_id": id},
            UpdateExpression="SET request_status=:s, code=:c",
            ExpressionAttributeValues={":s": status, ":c": status_code},
            ReturnValues="UPDATED_NEW",
        )

    def post_request(self, id, status, code):
        try:
            self.table.put_item(
                Item={"request_id": id, "request_status": status, "code": code}
            )
        except ClientError as e:
            # Not sure how to handle this exception
            print(e.response["Error"]["Message"])
            return False

        return True
