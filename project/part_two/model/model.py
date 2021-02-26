class Model:
    TABLE_NAME = "request"

    def get_request(self, id):
        """
        Gets the request from the DB.
        Returns True (has error) and error message if can't retrieve the
        request from DB, and False (has no error) and request json if retrieved
        request from DB
        """
        pass

    def update_request(self, id, status, status_code):
        """
        Update the request in the DB
        no try except blocks because this update isn't critical
        and won't result in different return values
        """
        pass

    def post_request(self, id, status, code):
        # Insert request into the DB
        pass
