import boto3
import time
from .model import Model
from botocore.exceptions import ClientError


class DynamoDB(Model):
    def __init__(self):
        """Initializes the instance.

        Creates DynamoDB Table if table doesn't exist in database.
        Sleeps for 5 seconds after table creation request to avoid
        requesting to insert into table before the table is created.
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
        """Gets the request data from the database table with the records id.

        Parameters
        ----------
        id : int
            The id of the request record we want to retrive from the DB

        Returns
        ------
        True (has error) and error message if can't retrieve the
        request from DB, and False (has no error) and request json if retrieved
        request from DB
        """
        try:
            response = self.table.get_item(Key={"request_id": id})
        except ClientError as e:
            # Handle exception
            return True, e.response["Error"]["Message"]

        if "Item" not in response:
            return True, f"{id} doesn't exist"

        return False, response["Item"]

    def update_request(self, id, status, code):
        """Update the request record in the DB

        Parameters
        ----------
        id : int
            The id of the request record we want to update
        status : str
            The status of the request (e.g. received, in progress, completed)
        code : int
            An integer value corresponding to a request status (e.g. 1 for received)

        Returns
        ------
        None
        """
        self.table.update_item(
            Key={"request_id": id},
            UpdateExpression="SET request_status=:s, code=:c",
            ExpressionAttributeValues={":s": status, ":c": code},
            ReturnValues="UPDATED_NEW",
        )

    def post_request(self, id, status, code):
        """Inserts new request into the DB

        Parameters
        ----------
        id : int
            The id of the new request record
        status : str
            The status of the request (e.g. received, in progress, completed)
        code : int
            An integer value corresponding to a request status (e.g. 1 for received)

        Returns
        ------
        True if record was successfully added, false if couldn't add record
        """
        try:
            self.table.put_item(
                Item={"request_id": id, "request_status": status, "code": code}
            )
        except ClientError as e:
            # Not sure how to handle this exception
            print(e.response["Error"]["Message"])
            return False

        return True
