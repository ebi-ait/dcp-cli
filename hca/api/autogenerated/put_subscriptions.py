"""This file is autogenerated according to HCA api spec. DON'T TOUCH!"""
from ...added_command import AddedCommand

class PutSubscriptions(AddedCommand):
    """Class containing info to reach the get endpoint of files."""

    @classmethod
    def _get_base_url(cls):
        return "https://hca-dss.czi.technology/v1"

    @classmethod
    def get_command_name(cls):
        return "put-subscriptions"

    @classmethod
    def _get_endpoint_info(cls):
        return {u'positional': [], u'seen': False, u'options': {u'query': {u'hierarchy': [u'query'], u'in': u'body', u'description': u'Elasticsearch query that will trigger the callback.', u'required_for': [u'/subscriptions'], u'format': None, u'pattern': None, u'array': False, u'required': True, u'type': u'object', u'metavar': None}, u'replica': {u'hierarchy': [u'replica'], u'in': u'query', u'description': u'Replica to write to. Can be one of aws, gcp, or azure.', u'required_for': [u'/subscriptions'], u'format': None, u'pattern': None, u'array': False, u'required': True, u'type': u'string', u'metavar': None}, u'callback_url': {u'hierarchy': [u'callback_url'], u'in': u'body', u'description': u'Url to send request to when a bundle comes in that matches this query.', u'required_for': [u'/subscriptions'], u'format': u'url', u'pattern': None, u'array': False, u'required': True, u'type': u'string', u'metavar': None}}, u'description': u'Create a new event subscription. Every time a new bundle version matches this query,\na request is sent to callback_url.\n'}
