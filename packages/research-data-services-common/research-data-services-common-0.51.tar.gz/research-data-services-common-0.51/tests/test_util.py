import unittest
import json

from RDS import LoginService, OAuth2Service, User, Token, OAuth2Token, Util


class Test_Util(unittest.TestCase):
    def setUp(self):
        self.service1 = LoginService(
            servicename="MusterService",
            implements=["fileStorage"])
        self.service2 = LoginService(
            servicename="BetonService",
            implements=["fileStorage"])
        self.oauthservice1 = OAuth2Service.from_service(
            self.service1,
            "http://localhost:5000/oauth/authorize",
            "http://localhost:5000/oauth/refresh",
            "ABC",
            "XYZ",
        )

        self.oauthservice2 = OAuth2Service.from_service(
            self.service2,
            "http://localhost:5000/oauth/authorize",
            "http://localhost:5000/oauth/refresh",
            "DEF",
            "MNO",
        )

        self.user1 = User("Max Mustermann")
        self.user2 = User("Mimi Mimikri")

        self.token1 = Token(self.user1, self.service1, "ABC")
        self.token2 = Token(self.user1, self.service2, "DEF")

        self.oauthtoken1 = OAuth2Token(
            self.user1, self.oauthservice1, "ABC", "XYZ")
        self.oauthtoken2 = OAuth2Token(
            self.user1, self.oauthservice2, "DEF", "UVW")

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            Util.load_class_from_json(123)

        with self.assertRaises(ValueError):
            Util.load_class_from_json([])

        with self.assertRaises(ValueError):
            Util.load_class_from_json("")

        with self.assertRaises(ValueError):
            Util.load_class_from_json("Blub bla bla")

        with self.assertRaises(ValueError):
            Util.load_class_from_json(json.dumps({}))

        with self.assertRaises(ValueError):
            jsonStr = json.dumps(self.token1)
            data = json.loads(jsonStr)
            del data["type"]
            Util.load_class_from_json(json.dumps(data))

        with self.assertRaises(ValueError):
            Util.initialize_object_from_json(123)

        with self.assertRaises(ValueError):
            Util.initialize_object_from_json([])

        with self.assertRaises(ValueError):
            Util.initialize_object_from_json("")

        with self.assertRaises(ValueError):
            Util.initialize_object_from_json("blub bla bla")

    def test_load_class_from_json(self):
        self.assertEqual(
            Util.load_class_from_json(json.dumps(self.service1)),
            self.service1.__class__,
            msg=json.dumps(self.service1),
        )
        self.assertEqual(
            Util.load_class_from_json(json.dumps(self.oauthservice1)),
            self.oauthservice1.__class__,
        )

        self.assertEqual(
            Util.load_class_from_json(json.dumps(
                self.token1)), self.token1.__class__
        )
        self.assertEqual(
            Util.load_class_from_json(json.dumps(self.oauthtoken1)),
            self.oauthtoken1.__class__,
        )

        self.assertEqual(
            Util.load_class_from_json(json.dumps(
                self.user1)), self.user1.__class__
        )

    def test_load_class_from_dict(self):
        # currently nowhere used.
        pass

    def test_initialize_object(self):
        self.assertEqual(
            Util.initialize_object_from_json(
                json.dumps(self.token1)), self.token1
        )
        self.assertEqual(
            Util.initialize_object_from_json(json.dumps(self.oauthtoken1)),
            self.oauthtoken1,
        )

        self.assertEqual(
            Util.initialize_object_from_json(
                json.dumps(self.service1)), self.service1
        )
        self.assertEqual(
            Util.initialize_object_from_json(json.dumps(self.oauthservice1)),
            self.oauthservice1,
        )

        self.assertEqual(
            Util.initialize_object_from_json(
                json.dumps(self.user1)), self.user1
        )

    def test_init_objects(self):
        self.assertEqual(Util.getServiceObject(
            json.dumps(self.oauthservice1)), self.oauthservice1)
        svc1 = LoginService(servicename="MusterService",
                            implements=["fileStorage"])
        self.assertEqual(Util.getServiceObject(json.dumps(svc1)), svc1)
        self.assertNotEqual(Util.getServiceObject(
            json.dumps(svc1)).__class__, self.oauthservice1.__class__)
        self.assertEqual(Util.getUserObject(
            json.dumps(self.user1)), self.user1)
        self.assertEqual(Util.getTokenObject(
            json.dumps(self.token1)), self.token1)

    def test_parseUserId(self):
        user = ("port-owncloud", "admin", "huhu")
        example = "{}://{}:{}".format(*user)
        self.assertEqual(Util.parseUserId(example), user)

        user = ("port-owncloud", "admin", "huhu")
        example = "{}://{}:{}".format(*user)
        self.assertEqual(Util.parseUserId(example), user)

        user = ("port-owncloud", "admin", None)
        example = "{}://{}:{}".format(*user)
        self.assertEqual(Util.parseUserId(example), user)

        user = ("port-owncloud", "admin", "None")
        example = "{}://{}:{}".format(*user)
        self.assertEqual(Util.parseUserId(example),
                         ("port-owncloud", "admin", None))

        user = ("port-owncloud", "", "")
        example = "{}://{}:{}".format(*user)
        self.assertEqual(Util.parseUserId(example),
                         ("port-owncloud", None, None))

        user = ("port-owncloud", "", "")
        example = "{}://{}:{}".format(*user)
        self.assertEqual(Util.parseUserId(example),
                         ("port-owncloud", None, None))

    def test_parseToken(self):
        user1 = User("MaxMustermann")
        service1 = LoginService(
            servicename="MusterService", implements=["fileStorage"])
        token1 = Token(user1, service1, "ABC")

        serviceport = "{}".format(token1.service.servicename)
        data = {
            "userId": "port-{}://{}:{}".format("musterservice", "MaxMustermann", "ABC")}

        self.assertEqual(Util.parseToken(token1), data)
