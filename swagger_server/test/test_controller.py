from swagger_server.test import BaseTestCase


class TestGuiControllerIntegration(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.client = self.app.test_client()
        # Inizializza dati di test nel DB mock
        self.mongo.db.repositories.insert_one({
            "_id": "user/repo1",
            "data": {
                "full_name": "user/repo1",
                "language": "Python",
                "private": False,
                "updated_at": "2025-01-01T00:00:00",
                "stars_count": 10,
            }
        })

    def tearDown(self):
        super().tearDown()
        self.mongo.db.repositories.delete_many({})

    def test_get_repositories(self):
        # Chiamata all’endpoint esposto dal tuo controller
        response = self.client.get("/repositories?page=1")
        data = self.assert_json_response(response, 200)

        self.assertEqual(data["total_elements"], 1)
        self.assertEqual(data["items"][0]["full_name"], "user/repo1")

    def test_get_repository(self):
        # Chiamata all’endpoint esposto dal tuo controller
        response = self.client.get("/repositories/user/repo1")
        data = self.assert_json_response(response, 200)
