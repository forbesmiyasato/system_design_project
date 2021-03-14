database = "dynamodb"

if database == "dynamodb":
    from .dynamo_model import DynamoDB as model
else:
    raise ValueError("No appropriate database configured.")

database_model = model()


def get_model():
    return database_model
