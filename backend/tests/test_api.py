import io
import tempfile
import unittest
from pathlib import Path

from app import create_app
from app.extensions import db
from app.models import ShareLink, utcnow
from app.services.rate_limit_service import rate_limiter


class SecureTransferApiTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.app = create_app(
            {
                "TESTING": True,
                "AUTO_INIT_DB": False,
                "SQLALCHEMY_DATABASE_URI": "sqlite://",
                "SECRET_KEY": "test-secret",
                "JWT_SECRET_KEY": "test-jwt-secret",
                "STORAGE_ROOT": Path(self.temp_dir.name) / "storage",
                "LOGIN_RATE_LIMIT_ATTEMPTS": 2,
                "LOGIN_RATE_LIMIT_WINDOW_SECONDS": 60,
                "UPLOAD_RATE_LIMIT_REQUESTS": 2,
                "UPLOAD_RATE_LIMIT_WINDOW_SECONDS": 60,
                "DEFAULT_SHARE_LINK_TTL_MINUTES": 15,
                "MAX_SHARE_LINK_TTL_MINUTES": 60,
                "DEFAULT_SHARE_LINK_MAX_DOWNLOADS": 1,
                "MAX_SHARE_LINK_MAX_DOWNLOADS": 5,
            }
        )
        rate_limiter.reset()

        with self.app.app_context():
            db.create_all()

        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        rate_limiter.reset()
        self.temp_dir.cleanup()

    def test_full_transfer_lifecycle(self):
        token = self.register_user("engineer", "password123")

        upload_response = self.client.post(
            "/api/v1/files",
            headers=self.auth_header(token),
            data={"file": (io.BytesIO(b"quarterly plan"), "plan.txt")},
            content_type="multipart/form-data",
        )
        self.assertEqual(upload_response.status_code, 201)
        file_id = upload_response.get_json()["data"]["file"]["id"]

        list_response = self.client.get("/api/v1/files", headers=self.auth_header(token))
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(len(list_response.get_json()["data"]["files"]), 1)

        dashboard_response = self.client.get(
            "/api/v1/dashboard", headers=self.auth_header(token)
        )
        self.assertEqual(dashboard_response.status_code, 200)
        self.assertEqual(
            dashboard_response.get_json()["data"]["metrics"]["totalFiles"], 1
        )

        download_response = self.client.get(
            f"/api/v1/files/{file_id}/download",
            headers=self.auth_header(token),
        )
        self.assertEqual(download_response.status_code, 200)
        self.assertEqual(download_response.data, b"quarterly plan")
        download_response.close()

        delete_response = self.client.delete(
            f"/api/v1/files/{file_id}",
            headers=self.auth_header(token),
        )
        self.assertEqual(delete_response.status_code, 200)

        final_list = self.client.get("/api/v1/files", headers=self.auth_header(token))
        self.assertEqual(final_list.get_json()["data"]["files"], [])

    def test_file_isolation_between_users(self):
        first_token = self.register_user("owner", "password123")
        second_token = self.register_user("viewer", "password123")

        upload_response = self.client.post(
            "/api/v1/files",
            headers=self.auth_header(first_token),
            data={"file": (io.BytesIO(b"private artifact"), "artifact.txt")},
            content_type="multipart/form-data",
        )
        file_id = upload_response.get_json()["data"]["file"]["id"]

        forbidden_download = self.client.get(
            f"/api/v1/files/{file_id}/download",
            headers=self.auth_header(second_token),
        )
        self.assertEqual(forbidden_download.status_code, 404)

    def test_expiring_share_link_allows_external_download_without_credentials(self):
        token = self.register_user("owner", "password123")
        file_id = self.upload_file(token, "external.txt", b"external recipient payload")

        share_response = self.client.post(
            f"/api/v1/files/{file_id}/shares",
            headers=self.auth_header(token),
            json={"expiresInMinutes": 5, "maxDownloads": 1},
        )
        self.assertEqual(share_response.status_code, 201)

        share_url = share_response.get_json()["data"]["shareLink"]["shareUrl"]
        share_token = share_url.split("/shares/")[1].split("/download")[0]

        external_download = self.client.get(f"/api/v1/shares/{share_token}/download")
        self.assertEqual(external_download.status_code, 200)
        self.assertEqual(external_download.data, b"external recipient payload")
        external_download.close()

        exhausted_download = self.client.get(f"/api/v1/shares/{share_token}/download")
        self.assertEqual(exhausted_download.status_code, 410)

    def test_expired_share_link_is_rejected(self):
        token = self.register_user("owner", "password123")
        file_id = self.upload_file(token, "expired.txt", b"stale data")

        share_response = self.client.post(
            f"/api/v1/files/{file_id}/shares",
            headers=self.auth_header(token),
        )
        self.assertEqual(share_response.status_code, 201)
        share_url = share_response.get_json()["data"]["shareLink"]["shareUrl"]
        share_token = share_url.split("/shares/")[1].split("/download")[0]

        with self.app.app_context():
            share_link = ShareLink.query.first()
            share_link.expires_at = utcnow().replace(year=utcnow().year - 1)
            db.session.commit()

        expired_download = self.client.get(f"/api/v1/shares/{share_token}/download")
        self.assertEqual(expired_download.status_code, 410)

    def test_login_rate_limit_triggers(self):
        self.register_user("throttle", "password123")

        first_attempt = self.client.post(
            "/api/v1/auth/login",
            json={"username": "throttle", "password": "wrong-password"},
        )
        second_attempt = self.client.post(
            "/api/v1/auth/login",
            json={"username": "throttle", "password": "wrong-password"},
        )
        third_attempt = self.client.post(
            "/api/v1/auth/login",
            json={"username": "throttle", "password": "wrong-password"},
        )

        self.assertEqual(first_attempt.status_code, 401)
        self.assertEqual(second_attempt.status_code, 401)
        self.assertEqual(third_attempt.status_code, 429)

    def test_upload_rate_limit_triggers(self):
        token = self.register_user("uploader", "password123")

        first_upload = self.upload_file(token, "one.txt", b"1")
        second_upload = self.upload_file(token, "two.txt", b"2")
        third_upload = self.client.post(
            "/api/v1/files",
            headers=self.auth_header(token),
            data={"file": (io.BytesIO(b"3"), "three.txt")},
            content_type="multipart/form-data",
        )

        self.assertTrue(first_upload)
        self.assertTrue(second_upload)
        self.assertEqual(third_upload.status_code, 429)

    def register_user(self, username, password):
        response = self.client.post(
            "/api/v1/auth/register",
            json={"username": username, "password": password},
        )
        self.assertEqual(response.status_code, 201)
        return response.get_json()["data"]["token"]

    @staticmethod
    def auth_header(token):
        return {"Authorization": f"Bearer {token}"}

    def upload_file(self, token, filename, contents):
        response = self.client.post(
            "/api/v1/files",
            headers=self.auth_header(token),
            data={"file": (io.BytesIO(contents), filename)},
            content_type="multipart/form-data",
        )
        self.assertEqual(response.status_code, 201)
        return response.get_json()["data"]["file"]["id"]
