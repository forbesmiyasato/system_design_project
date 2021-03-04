from .model import Model


class PostgreSQL(Model):
    def __init__(self):
        """
        Initializes the class.
        Creates PostgreSQL Table if table doesn't exist.
        """

    def get_request(self, id):
        print(self.TABLE_NAME)

    def update_request(self, id, status, code):
        pass

    def post_request(self, id, status, code):
        pass
