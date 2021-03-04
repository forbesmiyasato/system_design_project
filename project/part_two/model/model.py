class Model:
    """
    A class used as an abstraction of database operations

    Attributes
    ----------
    TABLE_NAME: str
        The table name in the database

    Methods
    -------
    get_request(id)
        Gets the request data from the database table with the records id.

    update_request(id, status, status_code)
        Updates the request record

    post_request(id, status, code)
        Inserts a new request record
    """

    TABLE_NAME = "request"

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
        pass

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
        pass

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
        pass
