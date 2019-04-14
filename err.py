class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


def validate_body_contains(keys, body):
    """
    Ensure the body is not None and ensure all keys exist in the body and are not None. Throws 404 if they don't exist
    """
    if body is None:
        raise InvalidUsage('post user body not given', status_code=404)
    try:
        vals = []
        for key in keys:
            vals.append(body[key])

        if None in vals:
            raise InvalidUsage("value not given for all keys " + str(keys), 404)
    except KeyError:
        raise InvalidUsage("All keys not provided " + str(keys), 404)
