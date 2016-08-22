import json

from django.test import SimpleTestCase
from djangopeople.django_openidconsumer.util import OpenID
from openid.consumer.discover import OpenIDServiceEndpoint
from openid.yadis.manager import YadisServiceManager

from ..serializers import JSONEncoder, JSONSerializer


class JSONEncoderTests(SimpleTestCase):
    def test_openid(self):
        self.assertEqual(
            json.loads(JSONEncoder().encode({'k': OpenID(openid='a', issued='b')})),
            {"k": {"openid": "a", "attrs": {}, "sreg_": {}, "ax_": {}, "issued": "b", "__class__": "OpenID"}}
        )

    def test_openidserviceendpoint(self):
        self.assertEqual(
            json.loads(JSONEncoder().encode({'k': OpenIDServiceEndpoint()})),
            {"k": {
                "type_uris": [], "claimed_id": None, "canonicalID": None,
                "__class__": "OpenIDServiceEndpoint", "used_yadis": False,
                "server_url": None, "local_id": None, "display_identifier": None,
            }}
        )

    def test_yadisservicemanager(self):
        manager = YadisServiceManager(starting_url='a', yadis_url='b', services='c', session_key='d')
        self.assertEqual(
            json.loads(JSONEncoder().encode({'k': manager})),
            {"k": {
                "services": ["c"], "starting_url": "a", "session_key": "d",
                "__class__": "YadisServiceManager", "yadis_url": "b",
            }}
        )


class JSONSerializerTests(SimpleTestCase):
    def test_openidserviceendpoint(self):
        endpoint = OpenIDServiceEndpoint()
        endpoint2 = JSONSerializer().loads(JSONSerializer().dumps({'k': endpoint}))
        self.assertIsInstance(endpoint2['k'], OpenIDServiceEndpoint)
