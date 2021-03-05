database = "dynamodb"

if database == "postgresql":
    from .postgres_model import PostgreSQL as model
elif database == "dynamodb":
    from .dynamo_model import DynamoDB as model
else:
    raise ValueError("No appropriate database configured.")

database_model = model()


def get_model():
    return database_model
