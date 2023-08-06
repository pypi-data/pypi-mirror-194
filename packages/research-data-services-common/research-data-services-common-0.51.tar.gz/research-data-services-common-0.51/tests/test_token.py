import unittest
import json

from RDS import Token, LoginToken, OAuth2Token, User, LoginService, OAuth2Service, FileTransferMode, FileTransferArchive, BaseService
from RDS import Util


class TestToken(unittest.TestCase):
    def setUp(self):
        self.user1 = User("Max Mustermann")
        self.user2 = User("12345")

        self.service1 = LoginService(
            servicename="MusterService", implements=["fileStorage"])
        self.service2 = LoginService(
            servicename="BetonService", implements=["fileStorage"])

        self.token1 = Token(self.user1, self.service1, "ABC")
        self.token2 = Token(self.user1, self.service2, "DEF")

        self.oauthservice1 = OAuth2Service(
            servicename="MusterService", implements=[
                "fileStorage"], fileTransferMode=FileTransferMode.active, fileTransferArchive=FileTransferArchive.none,
            authorize_url="http://localhost/oauth/authorize",
            refresh_url="http://localhost/oauth/token",
            client_id="MNO",
            client_secret="UVW",
        )
        self.oauthservice2 = OAuth2Service(
            servicename="BetonService", implements=[
                "fileStorage"], fileTransferMode=FileTransferMode.active, fileTransferArchive=FileTransferArchive.none,
            authorize_url="http://owncloud/oauth/authorize",
            refresh_url="http://owncloud/oauth/token",
            client_id="UVP",
            client_secret="OMN",
        )

        self.oauthtoken1 = OAuth2Token(
            self.user1, self.oauthservice1, "ABC", "XYZ")
        self.oauthtoken2 = OAuth2Token(
            self.user1, self.oauthservice2, "DEF", "UVW")

    def test_compare_tokens(self):
        t1 = Token(self.user1, self.service1, "ABC")
        t2 = Token(self.user1, self.service1, "ABC")
        t3 = Token(self.user1, self.service2, "ABC")
        t4 = Token(self.user1, self.service1, "QWERT")
        t5 = Token(self.user2, self.service2, "ABC")

        ot1 = OAuth2Token(self.user1, self.oauthservice1, "ABC", "XYZ")
        ot2 = OAuth2Token(self.user1, self.oauthservice1, "ABC", "XYZ")
        ot3 = self.oauthtoken2 = OAuth2Token(
            self.user1, self.oauthservice2, "DEF", "UVW"
        )
        ot4 = OAuth2Token(self.user1, self.oauthservice1, "QWE", "RTZ")

        self.assertEqual(t1, t2)
        self.assertNotEqual(t3, t2)
        self.assertEqual(t1, t4)
        self.assertNotEqual(t1, t5)

        self.assertFalse(t1 is t2)

        self.assertEqual(ot1, ot2)
        self.assertNotEqual(ot3, ot2)
        self.assertEqual(ot1, ot4)

        self.assertEqual(t1, ot1)

    def test_token_empty_string(self):
        with self.assertRaises(ValueError):
            Token(None, None, "")

        with self.assertRaises(ValueError):
            Token(self.user1, None, "")

        with self.assertRaises(ValueError):
            Token(self.user1, None, "ABC")

        with self.assertRaises(ValueError):
            OAuth2Token(self.user1, None, "", "")

        # refresh_token is the only parameter, which can be empty
        self.assertIsInstance(
            OAuth2Token(self.user1, self.oauthservice1, "ABC"), OAuth2Token
        )
        self.assertIsInstance(OAuth2Token(
            self.user1, self.oauthservice2, "ABC"), Token)

        with self.assertRaises(ValueError):
            OAuth2Token(self.user1, self.oauthservice1, "")

        with self.assertRaises(ValueError):
            OAuth2Token(self.user1, self.oauthservice1, "", "")

        with self.assertRaises(ValueError):
            OAuth2Token(self.user1, None, "ABC", "")

        with self.assertRaises(ValueError):
            OAuth2Token(self.user1, None, "", "X_ABC")

        with self.assertRaises(ValueError):
            OAuth2Token(self.user1, self.oauthservice1, "", "X_ABC")

        with self.assertRaises(ValueError):
            OAuth2Token(self.user1, None, "ABC", "X_ABC")

    def test_token_equal(self):
        self.assertEqual(self.token1, self.token1)
        self.assertNotEqual(self.token1, self.token2)

        self.assertEqual(self.oauthtoken1, self.oauthtoken1)
        self.assertEqual(self.oauthtoken2, self.oauthtoken2)

        self.assertEqual(
            self.token1, self.oauthtoken1, msg=f"\n{self.token1}\n {self.oauthtoken1}"
        )
        self.assertEqual(self.oauthtoken1, self.token1)

        self.assertIsInstance(self.oauthtoken1, Token)

    def test_token_json(self):
        dump = json.dumps(self.token1)
        # self.assertEqual(dump, json.dumps(expected))
        self.assertEqual(Token.from_json(dump), self.token1)

        expected = {
            "type": "OAuth2Token",
            "data": {
                "service": self.service1,
                "access_token": self.oauthtoken1.access_token,
                "refresh_token": self.oauthtoken1.refresh_token,
                "expiration_date": str(self.oauthtoken1.expiration_date),
            },
        }
        dump = json.dumps(self.oauthtoken1)
        # self.assertEqual(dump, json.dumps(expected))
        self.assertEqual(OAuth2Token.from_json(
            dump), self.oauthtoken1, msg=dump)

    def test_logintoken(self):
        user1 = User("Max Mustermann")
        user2 = User("12345")

        service1 = LoginService(
            servicename="MusterService", implements=["fileStorage"])
        service2 = LoginService(servicename="BetonService", implements=[
                                "fileStorage"], userId=False)
        service3 = LoginService(servicename="FahrService", implements=[
                                "fileStorage"], password=False)
        service4 = LoginService(
            servicename="TaxiService", implements=["fileStorage"], userId=False, password=False)

        with self.assertRaises(ValueError):
            LoginToken(None, service1, "")

        with self.assertRaises(ValueError):
            LoginToken(user1, service1, "")

        with self.assertRaises(ValueError):
            LoginToken(None, service1, "DEF")

        with self.assertRaises(ValueError):
            LoginToken(None, service2, "")

        with self.assertRaises(ValueError):
            LoginToken(user1, service2, "")

        LoginToken(None, service2, "DEF")

        with self.assertRaises(ValueError):
            LoginToken(None, service3, "")

        LoginToken(user1, service3, "")
        LoginToken(user1, service3, None)
        LoginToken(user1, service3, "DEF")

        with self.assertRaises(ValueError):
            LoginToken(None, service3, "DEF")

        LoginToken(None, service4, None)
        LoginToken(None, service4, "")
        LoginToken(user1, service4, "")
        LoginToken(None, service4, "DEF")

        Token(user1, service1, "DEF")
        Token(user1, service3, "DEF")

    def test_token_service_init(self):
        user1 = User("Max Mustermann")
        service1 = BaseService(servicename="MusterService",
                               implements=["fileStorage"])
        service2 = LoginService(
            servicename="BetonService", implements=["fileStorage"], userId=True, password=False)

        LoginToken(user1, service2, "")

        with self.assertRaises(ValueError):
            Token(user1, service1, "")

    def test_initToken(self):
        self.assertEqual(self.oauthtoken1, Util.initToken(
            self.oauthtoken1.to_json()))
        self.assertEqual(self.oauthtoken1, Util.initToken(
            self.oauthtoken1.to_dict()))
        self.assertEqual(self.oauthtoken1.expiration_date,
                         Util.initToken(self.oauthtoken1.to_json()).expiration_date)
        self.assertEqual(self.oauthtoken1.expiration_date,
                         Util.initToken(self.oauthtoken1.to_dict()).expiration_date)
        self.assertTrue(isinstance(Util.initToken(
            self.oauthtoken1.to_json()), OAuth2Token))
        self.assertTrue(isinstance(Util.initToken(
            self.oauthtoken1.to_dict()), OAuth2Token))
        self.assertNotEqual(self.oauthtoken2, Util.initToken(
            self.oauthtoken1.to_json()))
