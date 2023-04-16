from base_test import BaseTest
from main import app


class TestMain(BaseTest):
    def test_home(self):
        with self.app() as c:
            resp = c.get('/')
            self.assertEquals(resp.status_code, 200)
            self.assertIn("<html", resp.text)

    def test_about(self):
        with self.app() as c:
            resp = c.get("/api/v1/1/1988-10-25")
            self.assertEquals(resp.status_code, 200)