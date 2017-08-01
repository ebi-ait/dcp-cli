from ...added_command import AddedCommand

class HeadFiles(AddedCommand):
    """Class containing info to reach the get endpoint of files."""

    @classmethod
    def _get_base_url(cls):
        return "https://hca-dss.czi.technology/v1"

    @classmethod
    def _get_endpoint_info(cls):
        return {u'positional': [{u'description': u'A RFC4122-compliant ID for the file.', u'format': None, u'pattern': None, u'required': True, u'argument': u'uuid', u'required_for': [u'/files/{uuid}'], u'type': u'string'}], u'seen': False, u'options': {u'version': {u'hierarchy': [u'version'], u'in': u'query', u'description': u'Timestamp of file creation in RFC3339.  If this is not provided, the latest version is returned.', u'required_for': [], u'format': u'date-time', u'pattern': None, u'array': False, u'required': False, u'type': u'string', u'metavar': None}}, u'body_params': {}, u'description': u"Given a file UUID, return the metadata for the latest version of that file.  If the version is provided, that\nversion's metadata is returned instead.  The metadata is returned in the headers.\n"}
