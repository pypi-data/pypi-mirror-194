import unittest
from RDS import BaseService, LoginService, OAuth2Service, FileTransferMode, FileTransferArchive
import base64
from urllib import parse


class TestService(unittest.TestCase):
    def setUp(self):
        self.service1 = BaseService(
            "MusterService", ["fileStorage"], FileTransferMode.active, FileTransferArchive.none)
        self.service2 = BaseService(
            "BetonService", ["fileStorage"], FileTransferMode.active, FileTransferArchive.none)
        self.service3 = BaseService(
            "FahrService", ["fileStorage"], FileTransferMode.active, FileTransferArchive.none)

        self.oauthservice1 = OAuth2Service.from_service(
            self.service1,
            "http://localhost:5000/oauth/authorize",
            "http://localhost:5000/oauth/refresh",
            "ABC",
            "XYZ",
        )
        self.oauthservice2 = OAuth2Service.from_service(
            self.service2,
            "http://localhost:5001/oauth/authorize",
            "http://localhost:5001/oauth/refresh",
            "DEF",
            "UVW",
        )
        self.oauthservice3 = OAuth2Service.from_service(
            self.service3,
            "http://localhost:5001/api/authorize",
            "http://localhost:5001/api/refresh",
            "GHI",
            "MNO",
        )

    def test_compare_service(self):
        s1 = BaseService(servicename="MusterService", implements=["fileStorage"],
                         fileTransferMode=FileTransferMode.active, fileTransferArchive=FileTransferArchive.none)
        s2 = BaseService(servicename="MusterService", implements=["metadata"],
                         fileTransferMode=FileTransferMode.passive, fileTransferArchive=FileTransferArchive.zip)
        s3 = BaseService(servicename="FahrService", implements=["fileStorage"],
                         fileTransferMode=FileTransferMode.active, fileTransferArchive=FileTransferArchive.none)

        os1 = OAuth2Service.from_service(
            s1,
            "http://localhost:5000/oauth/authorize",
            "http://localhost:5000/oauth/refresh",
            "ABC",
            "XYZ",
        )
        os2 = OAuth2Service.from_service(
            s2,
            "http://localhost:5000/oauth/authorize",
            "http://localhost:5000/oauth/refresh",
            "ABC",
            "XYZ",
        )
        os3 = OAuth2Service.from_service(
            s3,
            "http://localhost123:5000/oauth/authorize",
            "http://localhost123:5000/oauth/refresh",
            "WER",
            "DA",
        )
        os4 = OAuth2Service.from_service(
            s1,
            "http://localhost:5000/oauth/authorize",
            "http://localhost:5000/oauth/refresh",
            "QWE",
            "RTZ",
        )

        self.assertEqual(s1, s2)
        self.assertNotEqual(s1, s3)
        self.assertFalse(s1 is s2)

        self.assertEqual(os1, os2)
        self.assertEqual(os1, os4)
        self.assertNotEqual(os1, os3)

        self.assertEqual(s1, os1)

    def test_implements(self):
        with self.assertRaises(ValueError):
            LoginService(
                servicename="",
                implements=[],
                fileTransferMode=FileTransferMode.active,
                fileTransferArchive=FileTransferArchive.none
            )

        with self.assertRaises(ValueError):
            LoginService(
                servicename="",
                implements=["not_working"],
                fileTransferMode=FileTransferMode.active,
                fileTransferArchive=FileTransferArchive.none)
        with self.assertRaises(ValueError):
            LoginService(
                servicename="",
                implements=["metadata", "not_working"],
                fileTransferMode=FileTransferMode.active,
                fileTransferArchive=FileTransferArchive.none
            )
        with self.assertRaises(ValueError):
            LoginService(
                servicename="",
                implements=["metadata", "fileStorage", "not_working"],
                fileTransferMode=FileTransferMode.active,
                fileTransferArchive=FileTransferArchive.none
            )

        LoginService(
            servicename="TestService",
            implements=["fileStorage"],
            fileTransferMode=FileTransferMode.active,
            fileTransferArchive=FileTransferArchive.none
        )
        LoginService(
            servicename="TestService",
            implements=["fileStorage", "metadata"],
            fileTransferMode=FileTransferMode.active,
            fileTransferArchive=FileTransferArchive.none
        )

    def test_service(self):
        with self.assertRaises(ValueError):
            LoginService(
                servicename="",
                implements=[],
                fileTransferMode=FileTransferMode.active,
                fileTransferArchive=FileTransferArchive.none,
                userId="",
                password=""
            )

        with self.assertRaises(ValueError):
            LoginService(
                servicename="Service",
                implements=[],
                fileTransferMode=3,
                fileTransferArchive="",
                userId=False,
                password=False
            )

        with self.assertRaises(ValueError):
            LoginService(
                servicename="Service",
                implements=["not_working"],
                fileTransferMode=FileTransferMode.active,
                fileTransferArchive=FileTransferArchive.none,
                userId=False,
                password=False
            )

        with self.assertRaises(ValueError):
            LoginService(servicename="Service")

        LoginService(servicename="Service", implements=["fileStorage"])
        LoginService(servicename="Service", implements=[
                     "fileStorage"], fileTransferMode=FileTransferMode.active)
        LoginService(servicename="Service", implements=["fileStorage"], fileTransferMode=FileTransferMode.active,
                     fileTransferArchive=FileTransferArchive.none)
        LoginService(servicename="Service", implements=["fileStorage"], fileTransferMode=FileTransferMode.active,
                     fileTransferArchive=FileTransferArchive.none, userId=False)
        LoginService(servicename="Service", implements=["fileStorage"], fileTransferMode=FileTransferMode.active,
                     fileTransferArchive=FileTransferArchive.none, userId=True, password=False)
        LoginService(servicename="Service", implements=["fileStorage"], fileTransferMode=FileTransferMode.active,
                     fileTransferArchive=FileTransferArchive.none, userId=False, password=False)

        with self.assertRaises(ValueError):
            OAuth2Service(
                servicename="",
                implements=["fileStorage"],
                fileTransferMode=FileTransferMode.active,
                fileTransferArchive=FileTransferArchive.none,
                authorize_url="",
                refresh_url="",
                client_id="",
                client_secret=""
            )
            with self.assertRaises(ValueError):
                OAuth2Service(
                    servicename="MusterService",
                    implements=["fileStorage"],
                    fileTransferMode=FileTransferMode.active,
                    fileTransferArchive=FileTransferArchive.none,
                    authorize_url="",
                    refresh_url="",
                    client_id="",
                    client_secret=""
                )
            with self.assertRaises(ValueError):
                OAuth2Service(
                    servicename="",
                    implements=["fileStorage"],
                    fileTransferMode=FileTransferMode.active,
                    fileTransferArchive=FileTransferArchive.none,
                    authorize_url="http://localhost:5001/oauth/authorize",
                    refresh_url="",
                    client_id="",
                    client_secret=""
                )
            with self.assertRaises(ValueError):
                OAuth2Service(
                    servicename="",
                    implements=["fileStorage"],
                    fileTransferMode=FileTransferMode.active,
                    fileTransferArchive=FileTransferArchive.none,
                    authorize_url="",
                    refresh_url="http://localhost:5001/oauth/refresh",
                    client_id="",
                    client_secret=""
                )
            with self.assertRaises(ValueError):
                OAuth2Service(
                    servicename="",
                    implements=["fileStorage"],
                    fileTransferMode=FileTransferMode.active,
                    fileTransferArchive=FileTransferArchive.none,
                    authorize_url="",
                    refresh_url="",
                    client_id="ABC",
                    client_secret=""
                )
            with self.assertRaises(ValueError):
                OAuth2Service(
                    servicename="",
                    implements=["fileStorage"],
                    fileTransferMode=FileTransferMode.active,
                    fileTransferArchive=FileTransferArchive.none,
                    authorize_url="",
                    refresh_url="",
                    client_id="",
                    client_secret="XYZ"
                )
            with self.assertRaises(ValueError):
                OAuth2Service(
                    servicename="MusterService",
                    implements=["fileStorage"],
                    fileTransferMode=FileTransferMode.active,
                    fileTransferArchive=FileTransferArchive.none,
                    authorize_url="http://localhost:5001/oauth/authorize",
                    refresh_url="",
                    client_id="",
                    client_secret=""
                )
            with self.assertRaises(ValueError):
                OAuth2Service(
                    servicename="MusterService",
                    implements=["fileStorage"],
                    fileTransferMode=FileTransferMode.active,
                    fileTransferArchive=FileTransferArchive.none,
                    authorize_url="",
                    refresh_url="http://localhost:5001/oauth/refresh",
                    client_id="",
                    client_secret=""
                )
            with self.assertRaises(ValueError):
                OAuth2Service(
                    servicename="MusterService",
                    implements=["fileStorage"],
                    fileTransferMode=FileTransferMode.active,
                    fileTransferArchive=FileTransferArchive.none,
                    authorize_url="",
                    refresh_url="",
                    client_id="ABC",
                    client_secret=""
                )
            with self.assertRaises(ValueError):
                OAuth2Service(
                    servicename="MusterService",
                    implements=["fileStorage"],
                    fileTransferMode=FileTransferMode.active,
                    fileTransferArchive=FileTransferArchive.none,
                    authorize_url="",
                    refresh_url="",
                    client_id="",
                    client_secret="XYZ"
                )
            with self.assertRaises(ValueError):
                OAuth2Service(
                    servicename="MusterService",
                    implements=["fileStorage"],
                    fileTransferMode=FileTransferMode.active,
                    fileTransferArchive=FileTransferArchive.none,
                    authorize_url="http://localhost:5001/oauth/refresh",
                    refresh_url="",
                    client_id="",
                    client_secret=""
                )
            with self.assertRaises(ValueError):
                OAuth2Service(
                    servicename="MusterService",
                    implements=["fileStorage"],
                    fileTransferMode=FileTransferMode.active,
                    fileTransferArchive=FileTransferArchive.none,
                    authorize_url="http://localhost:5001/oauth/authorize",
                    refresh_url="http://localhost:5001/oauth/refresh",
                    client_id="",
                    client_secret="",
                )

            # same input for authorize and refresh
            with self.assertRaises(ValueError):
                OAuth2Service(
                    servicename="MusterService",
                    implements=["fileStorage"],
                    fileTransferMode=FileTransferMode.active,
                    fileTransferArchive=FileTransferArchive.none,
                    authorize_url="http://localhost:5001/oauth/authorize",
                    refresh_url="http://localhost:5001/oauth/refresh",
                    client_id="",
                    client_secret="",
                )

    def test_service_no_protocoll(self):
        # no protocoll
        with self.assertRaises(ValueError):
            OAuth2Service(
                servicename="MusterService",
                implements=["fileStorage"],
                fileTransferMode=FileTransferMode.active,
                fileTransferArchive=FileTransferArchive.none,
                authorize_url="localhost",
                refresh_url="http://localhost:5001/oauth/refresh",
                client_id="ABC",
                client_secret="XYZ",
            )
            OAuth2Service(
                servicename="MusterService",
                implements=["fileStorage"],
                fileTransferMode=FileTransferMode.active,
                fileTransferArchive=FileTransferArchive.none,
                authorize_url="localhost:5001",
                refresh_url="http://localhost:5001/oauth/authorize",
                client_id="ABC",
                client_secret="XYZ",
            )
            OAuth2Service(
                servicename="MusterService",
                implements=["fileStorage"],
                fileTransferMode=FileTransferMode.active,
                fileTransferArchive=FileTransferArchive.none,
                authorize_url="localhost:5001/oauth/authorize",
                refresh_url="http://localhost:5001/oauth/refresh",
                client_id="ABC",
                client_secret="XYZ",
            )
            OAuth2Service(
                servicename="MusterService",
                implements=["fileStorage"],
                fileTransferMode=FileTransferMode.active,
                fileTransferArchive=FileTransferArchive.none,
                authorize_url="http://localhost:5001",
                refresh_url="localhost:5001/oauth/refresh",
                client_id="ABC",
                client_secret="XYZ",
            )
            OAuth2Service(
                servicename="MusterService",
                implements=["fileStorage"],
                fileTransferMode=FileTransferMode.active,
                fileTransferArchive=FileTransferArchive.none,
                authorize_url="http://localhost:5001",
                refresh_url="localhost:5001/oauth/authorize",
                client_id="ABC",
                client_secret="XYZ",
            )

    def test_service_equal(self):
        # check if they are equal
        svc1 = OAuth2Service(
            servicename="MusterService",
            implements=["fileStorage"],
            fileTransferMode=FileTransferMode.active,
            fileTransferArchive=FileTransferArchive.none,
            authorize_url="http://localhost:5001",
            refresh_url="http://localhost:5001/oauth/refresh",
            client_id="ABC",
            client_secret="XYZ",
        )
        svc2 = OAuth2Service(
            servicename="MusterService",
            implements=["fileStorage"],
            fileTransferMode=FileTransferMode.active,
            fileTransferArchive=FileTransferArchive.none,
            authorize_url="http://localhost:5001",
            refresh_url="http://localhost:5001/oauth/refresh",
            client_id="ABC",
            client_secret="XYZ",
        )
        self.assertEqual(
            svc1, svc2, msg=f"Service1: {svc1}\n Service2: {svc2}")

        svc2 = OAuth2Service(
            servicename="musterservice",
            implements=["fileStorage"],
            fileTransferMode=FileTransferMode.active,
            fileTransferArchive=FileTransferArchive.none,
            authorize_url="http://localhost:5001",
            refresh_url="http://localhost:5001/oauth/refresh",
            client_id="ABC",
            client_secret="XYZ",
        )
        self.assertEqual(
            svc1, svc2, msg=f"Service1: {svc1}\n Service2: {svc2}")

        svc2 = OAuth2Service(
            servicename="musterService",
            implements=["fileStorage"],
            fileTransferMode=FileTransferMode.active,
            fileTransferArchive=FileTransferArchive.none,
            authorize_url="http://localhost:5001",
            refresh_url="http://localhost:5001/oauth/refresh",
            client_id="ABC",
            client_secret="XYZ",
        )
        self.assertEqual(
            svc1, svc2, msg=f"Service1: {svc1}\n Service2: {svc2}")

    def test_service_trailing_slash(self):
        # check if root dir is valid
        svc1 = OAuth2Service(
            servicename="MusterService",
            implements=["fileStorage"],
            fileTransferMode=FileTransferMode.active,
            fileTransferArchive=FileTransferArchive.none,
            authorize_url="http://localhost:5001",
            refresh_url="http://localhost:5001/oauth/refresh",
            client_id="ABC",
            client_secret="XYZ",
        )
        self.assertIsInstance(svc1, OAuth2Service)

        svc2 = OAuth2Service(
            servicename="MusterService",
            implements=["fileStorage"],
            fileTransferMode=FileTransferMode.active,
            fileTransferArchive=FileTransferArchive.none,
            authorize_url="http://localhost:5001/",
            refresh_url="http://localhost:5001/oauth/refresh/",
            client_id="ABC",
            client_secret="XYZ",
        )
        self.assertIsInstance(svc2, OAuth2Service)

        # check if they are equal
        self.assertEqual(
            svc1, svc2, msg=f"Service1: {svc1}\n Service2: {svc2}")

    def test_service_check_raises(self):
        svc1 = OAuth2Service(
            servicename="MusterService",
            implements=["fileStorage"],
            fileTransferMode=FileTransferMode.active,
            fileTransferArchive=FileTransferArchive.none,
            authorize_url="http://localhost:5001",
            refresh_url="http://localhost:5001/oauth/refresh",
            client_id="ABC",
            client_secret="XYZ",
        )

        from RDS import User, Token, OAuth2Token

        with self.assertRaises(ValueError):
            svc1.refresh(Token(User("Max Mustermann"), svc1, "ABC"))
            svc1.refresh("asd")
            svc1.refresh(123)

    def test_service_give_description(self):
        text = "This is a test description."

        svc1 = BaseService(
            servicename="MusterService",
            implements=["fileStorage"],
            fileTransferMode=FileTransferMode.active,
            fileTransferArchive=FileTransferArchive.none,
            description=text
        )

        self.assertEqual(svc1.description, text)
        self.assertNotEqual(svc1.description, "This is not valid.")
        self.assertEqual(svc1.to_dict().get("description"), text)
        self.assertEqual(BaseService.from_dict(
            svc1.to_dict()).description, text)
        self.assertEqual(BaseService.from_json(
            svc1.to_json()).description, text)

        svc1 = OAuth2Service(
            servicename="MusterService",
            implements=["fileStorage"],
            fileTransferMode=FileTransferMode.active,
            fileTransferArchive=FileTransferArchive.none,
            authorize_url="http://localhost:5001",
            refresh_url="http://localhost:5001/oauth/refresh",
            client_id="ABC",
            client_secret="XYZ",
            description=text
        )

        self.assertEqual(svc1.description, text)

        svc1 = LoginService(
            servicename="Service",
            implements=["fileStorage"],
            fileTransferMode=FileTransferMode.active,
            fileTransferArchive=FileTransferArchive.none,
            userId=False, password=False,
            description=text
        )

        self.assertEqual(svc1.description, text)

    def test_icon_post(self):
        svc1 = BaseService(
            servicename="owncloud",
            implements=["fileStorage"],
            fileTransferMode=FileTransferMode.active,
            fileTransferArchive=FileTransferArchive.none,
            icon="./tests/sciebo.png"
        )

        svc2 = BaseService.from_json(svc1.to_json())
        self.assertEqual(svc1.icon, svc2.icon)

        svc2 = BaseService.from_dict(svc1.to_dict())
        self.assertEqual(svc1.icon, svc2.icon)

    def test_icon(self):
        # if no icon was given, then it is okay.
        BaseService(
            servicename="owncloud",
            implements=["fileStorage"],
            fileTransferMode=FileTransferMode.active,
            fileTransferArchive=FileTransferArchive.none
        )

        # if a filepath was given, then it have to be exist.
        with self.assertRaises(FileNotFoundError):
            BaseService(
                servicename="owncloud",
                implements=["fileStorage"],
                fileTransferMode=FileTransferMode.active,
                fileTransferArchive=FileTransferArchive.none,
                icon="sciebo.png"
            )

        filename = "./tests/sciebo.png"

        with open(filename, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")

            svc1 = BaseService(
                servicename="owncloud",
                implements=["fileStorage"],
                fileTransferMode=FileTransferMode.active,
                fileTransferArchive=FileTransferArchive.none,
                icon=filename
            )
            self.assertEqual(f"data:image/png;base64,{b64}", svc1.icon)
            self.assertFalse(str(svc1.icon).find("b'") >= 0)
            self.assertFalse(str(svc1.icon).find("'") >= 0)

    def test_metadata_profile(self):
        # if a filepath was given, then it has to exist.
        with self.assertRaises(FileNotFoundError):
            BaseService(
                servicename="owncloud",
                implements=["fileStorage"],
                fileTransferMode=FileTransferMode.active,
                fileTransferArchive=FileTransferArchive.none,
                metadataProfile="sciebo.json"
            )

        filename = "./tests/test.json"

        with open(filename, 'r') as f:
            metadata = f.read()

            svc = BaseService(
                servicename="owncloud",
                implements=["fileStorage"],
                fileTransferMode=FileTransferMode.active,
                fileTransferArchive=FileTransferArchive.none,
                metadataProfile=filename
            )
            self.assertEqual(metadata, svc.metadataProfile)

    def test_url(self):
        infoUrl = "http://localhost"

        svc1 = BaseService(
            servicename="owncloud",
            implements=["fileStorage"],
            fileTransferMode=FileTransferMode.active,
            fileTransferArchive=FileTransferArchive.none,
            infoUrl=infoUrl
        )
        self.assertEqual(infoUrl, parse.unquote_plus(svc1.infoUrl))
        self.assertEqual(BaseService.from_json(
            svc1.to_json()).infoUrl, parse.quote_plus(infoUrl))
        self.assertNotEqual(BaseService.from_json(
            svc1.to_json()).infoUrl, infoUrl)

        svc1 = BaseService(
            servicename="owncloud",
            implements=["fileStorage"],
            fileTransferMode=FileTransferMode.active,
            fileTransferArchive=FileTransferArchive.none,
            infoUrl=None
        )

        self.assertEqual(svc1.infoUrl, "")

        svc1 = BaseService(
            servicename="owncloud",
            implements=["fileStorage"],
            fileTransferMode=FileTransferMode.active,
            fileTransferArchive=FileTransferArchive.none,
            infoUrl=""
        )

        self.assertEqual(svc1.infoUrl, "")

        svc1 = LoginService(
            servicename="owncloud",
            implements=["fileStorage"],
            fileTransferMode=FileTransferMode.active,
            fileTransferArchive=FileTransferArchive.none,
            userId=False,
            password=False,
            infoUrl=infoUrl
        )
        self.assertEqual(infoUrl, parse.unquote_plus(svc1.infoUrl))

        svc1 = LoginService(
            servicename="owncloud",
            implements=["fileStorage"],
            fileTransferMode=FileTransferMode.active,
            fileTransferArchive=FileTransferArchive.none,
            userId=False,
            password=False
        )
        self.assertEqual(svc1.infoUrl, "")

        svc1 = OAuth2Service(
            servicename="MusterService",
            implements=["fileStorage"],
            fileTransferMode=FileTransferMode.active,
            fileTransferArchive=FileTransferArchive.none,
            authorize_url="http://localhost:5001",
            refresh_url="http://localhost:5001/oauth/refresh",
            client_id="ABC",
            client_secret="XYZ",
            infoUrl=infoUrl
        )
        self.assertEqual(infoUrl, parse.unquote_plus(svc1.infoUrl))

    def test_displayname(self):
        displayname = "ownCloud"

        svc1 = BaseService(
            servicename="owncloud",
            implements=["fileStorage"],
            fileTransferMode=FileTransferMode.active,
            fileTransferArchive=FileTransferArchive.none,
            displayName=displayname
        )

        self.assertEqual(displayname, svc1.displayName)

        svc1 = LoginService(
            servicename="owncloud",
            implements=["fileStorage"],
            fileTransferMode=FileTransferMode.active,
            fileTransferArchive=FileTransferArchive.none,
            userId=False, password=False,
            displayName=displayname
        )

        self.assertEqual(displayname, svc1.displayName)
        self.assertNotEqual(displayname, svc1.servicename)
