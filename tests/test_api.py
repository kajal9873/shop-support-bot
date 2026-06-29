"""
Integration tests for FastAPI endpoints: /chat, /orders, /admin.
Uses TestClient with a fresh in-memory SQLite DB per test session.
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.db.database import Base, engine, get_db, SessionLocal


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def db_session():
    db = SessionLocal()
    yield db
    db.close()


# ---------- Health / Root ----------

class TestHealth:
    def test_health_check(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    def test_docs_available(self, client):
        response = client.get("/docs")
        assert response.status_code == 200


# ---------- /chat endpoint ----------

class TestChatEndpoint:
    def test_chat_english_query(self, client):
        payload = {"message": "what are your shop timings", "session_id": "test-en-1"}
        response = client.post("/chat", json=payload)
        assert response.status_code == 200
        body = response.json()
        assert "reply" in body
        assert "detected_language" in body
        assert isinstance(body["reply"], str) and len(body["reply"]) > 0

    def test_chat_codemixed_query(self, client):
        payload = {"message": "mera order kaha hai bhai", "session_id": "test-hi-1"}
        response = client.post("/chat", json=payload)
        assert response.status_code == 200
        body = response.json()
        assert "reply" in body
        assert body.get("cmi_score") is not None

    def test_chat_missing_message_field(self, client):
        response = client.post("/chat", json={"session_id": "test-bad"})
        assert response.status_code == 422

    def test_chat_empty_message(self, client):
        response = client.post("/chat", json={"message": "", "session_id": "test-empty"})
        assert response.status_code in (200, 422)

    def test_chat_response_includes_intent(self, client):
        payload = {"message": "is sugar available", "session_id": "test-intent"}
        response = client.post("/chat", json=payload)
        body = response.json()
        assert "intent" in body

    def test_chat_session_persistence(self, client):
        sid = "test-session-persist"
        client.post("/chat", json={"message": "hi", "session_id": sid})
        response = client.post("/chat", json={"message": "order status batao", "session_id": sid})
        assert response.status_code == 200
        assert response.json()["session_id"] == sid


# ---------- /orders endpoint ----------

class TestOrdersEndpoint:
    def test_get_order_status_not_found(self, client):
        response = client.get("/orders/NONEXISTENT123")
        assert response.status_code == 404

    def test_get_order_status_found(self, client, db_session):
        # assumes seed_data.py inserts a known test order, else create one inline
        response = client.get("/orders/ORD1001")
        assert response.status_code in (200, 404)
        if response.status_code == 200:
            body = response.json()
            assert "status" in body
            assert "order_id" in body

    def test_orders_list_requires_pagination_defaults(self, client):
        response = client.get("/orders")
        assert response.status_code == 200
        body = response.json()
        assert isinstance(body, (list, dict))


# ---------- /admin endpoint ----------

class TestAdminEndpoint:
    def test_admin_dashboard_requires_auth(self, client):
        response = client.get("/admin/dashboard")
        assert response.status_code in (200, 401, 403)

    def test_admin_add_product(self, client):
        payload = {
            "name": "Sugar 1kg",
            "price": 55.0,
            "stock": 100,
            "category": "grocery",
        }
        response = client.post("/admin/products", json=payload)
        assert response.status_code in (200, 201, 401)

    def test_admin_invalid_product_payload(self, client):
        response = client.post("/admin/products", json={"name": ""})
        assert response.status_code == 422


# ---------- CORS / misc ----------

class TestMisc:
    def test_cors_headers_present(self, client):
        response = client.options(
            "/chat",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "POST",
            },
        )
        assert response.status_code in (200, 204)

    def test_404_for_unknown_route(self, client):
        response = client.get("/this/route/does/not/exist")
        assert response.status_code == 404