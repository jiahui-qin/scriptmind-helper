"""API endpoint integration tests using FastAPI TestClient.

All MiMo API calls are mocked via unittest.mock.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import io
import json
import pytest
from unittest.mock import patch, MagicMock, PropertyMock
from fastapi.testclient import TestClient

from app.main import app
from app.database import get_db, Base, engine, SessionLocal

# ── Override the get_db dependency to use test DB ──────────────

def override_get_db():
    """Override get_db to use test session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# ── Fixtures ────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def setup_db():
    """Create tables before each test, drop after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# ── Helper ──────────────────────────────────────────────────────

def create_script_file(content: str) -> io.BytesIO:
    """Create an in-memory .txt file for upload testing."""
    return io.BytesIO(content.encode("utf-8"))


# ── Health Check ────────────────────────────────────────────────

class TestHealthCheck:
    """Tests for /health endpoint."""

    def test_health_returns_ok(self):
        """Test that health check returns 200 with ok status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["service"] == "scriptmind-ai"

    def test_root_returns_info(self):
        """Test that root endpoint returns API info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "ScriptMind AI API"


# ── Upload Endpoints ────────────────────────────────────────────

class TestUploadScript:
    """Tests for POST /api/v1/upload/script."""

    def test_upload_valid_txt_file(self):
        """Test uploading a valid .txt script file."""
        content = "张三：大家好\n李四：你好"
        file = create_script_file(content)
        response = client.post(
            "/api/v1/upload/script",
            files={"file": ("test_script.txt", file, "text/plain")},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["filename"] == "test_script.txt"
        assert data["file_size"] > 0
        assert "id" in data
        assert "created_at" in data

    def test_upload_non_txt_file_rejected(self):
        """Test that non-.txt files are rejected with 400."""
        file = io.BytesIO(b"some content")
        response = client.post(
            "/api/v1/upload/script",
            files={"file": ("script.pdf", file, "application/pdf")},
        )
        assert response.status_code == 400
        assert "Only .txt files" in response.json()["detail"]

    def test_upload_creates_database_record(self):
        """Test that upload creates a database record."""
        content = "测试角色：测试台词"
        file = create_script_file(content)
        response = client.post(
            "/api/v1/upload/script",
            files={"file": ("test.txt", file, "text/plain")},
        )
        assert response.status_code == 201
        data = response.json()
        script_id = data["id"]

        # Verify it can be retrieved
        get_response = client.get(f"/api/v1/upload/script/{script_id}")
        assert get_response.status_code == 200
        assert get_response.json()["filename"] == "test.txt"


class TestGetScript:
    """Tests for GET /api/v1/upload/script/{id}."""

    def test_get_existing_script(self):
        """Test retrieving an existing script by ID."""
        content = "A：测试内容"
        file = create_script_file(content)
        upload_resp = client.post(
            "/api/v1/upload/script",
            files={"file": ("script.txt", file, "text/plain")},
        )
        script_id = upload_resp.json()["id"]

        response = client.get(f"/api/v1/upload/script/{script_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == script_id
        assert data["filename"] == "script.txt"

    def test_get_nonexistent_script_404(self):
        """Test that getting a nonexistent script returns 404."""
        response = client.get("/api/v1/upload/script/99999")
        assert response.status_code == 404

    def test_get_nonexistent_script_message(self):
        """Test that 404 response includes a helpful message."""
        response = client.get("/api/v1/upload/script/99999")
        assert "not found" in response.json()["detail"].lower()


class TestListScripts:
    """Tests for GET /api/v1/upload/scripts."""

    def test_list_scripts_empty(self):
        """Test listing scripts when none exist."""
        response = client.get("/api/v1/upload/scripts")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_scripts_with_data(self):
        """Test listing scripts after uploading."""
        for i in range(3):
            file = create_script_file(f"Script {i}")
            client.post(
                "/api/v1/upload/script",
                files={"file": (f"script_{i}.txt", file, "text/plain")},
            )
        response = client.get("/api/v1/upload/scripts")
        assert response.status_code == 200
        assert len(response.json()) == 3


# ── Analysis Endpoints ──────────────────────────────────────────

class TestTriggerAnalysis:
    """Tests for POST /api/v1/analysis/{id}/analyze."""

    def test_trigger_analysis_existing_script(self):
        """Test triggering analysis on an existing script."""
        file = create_script_file("张三：你好")
        upload_resp = client.post(
            "/api/v1/upload/script",
            files={"file": ("script.txt", file, "text/plain")},
        )
        script_id = upload_resp.json()["id"]

        response = client.post(f"/api/v1/analysis/{script_id}/analyze")
        assert response.status_code == 202
        data = response.json()
        assert data["script_id"] == script_id
        assert data["status"] == "pending"

    def test_trigger_analysis_nonexistent_script(self):
        """Test triggering analysis on nonexistent script returns 404."""
        response = client.post("/api/v1/analysis/99999/analyze")
        assert response.status_code == 404


class TestGetAnalysis:
    """Tests for GET /api/v1/analysis/{id}."""

    def test_get_analysis_existing_script(self):
        """Test getting analysis results for an existing script."""
        file = create_script_file("张三：你好")
        upload_resp = client.post(
            "/api/v1/upload/script",
            files={"file": ("script.txt", file, "text/plain")},
        )
        script_id = upload_resp.json()["id"]

        response = client.get(f"/api/v1/analysis/{script_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["script_id"] == script_id
        assert "is_analyzed" in data
        assert "roles_count" in data
        assert "lines_count" in data
        assert "roles" in data

    def test_get_analysis_nonexistent_script(self):
        """Test getting analysis for nonexistent script returns 404."""
        response = client.get("/api/v1/analysis/99999")
        assert response.status_code == 404


# ── TTS Endpoints ───────────────────────────────────────────────

class TestTriggerTTS:
    """Tests for POST /api/v1/tts/{id}/synthesize."""

    def _upload_and_mark_analyzed(self) -> int:
        """Helper: upload a script and mark it as analyzed."""
        file = create_script_file("张三：你好\n李四：再见")
        upload_resp = client.post(
            "/api/v1/upload/script",
            files={"file": ("script.txt", file, "text/plain")},
        )
        script_id = upload_resp.json()["id"]

        # Manually mark as analyzed via direct DB access
        from app.models.script import Script
        db_session = SessionLocal()
        script = db_session.query(Script).filter(Script.id == script_id).first()
        script.is_analyzed = True
        db_session.commit()
        db_session.close()

        return script_id

    def test_trigger_tts_analyzed_script(self):
        """Test triggering TTS on an analyzed script."""
        script_id = self._upload_and_mark_analyzed()

        response = client.post(f"/api/v1/tts/{script_id}/synthesize")
        assert response.status_code == 202
        data = response.json()
        assert data["script_id"] == script_id
        assert data["status"] == "pending"

    def test_trigger_tts_unanalyzed_script_returns_400(self):
        """Test that TTS on unanalyzed script returns 400."""
        file = create_script_file("张三：你好")
        upload_resp = client.post(
            "/api/v1/upload/script",
            files={"file": ("script.txt", file, "text/plain")},
        )
        script_id = upload_resp.json()["id"]

        response = client.post(f"/api/v1/tts/{script_id}/synthesize")
        assert response.status_code == 400
        assert "analyzed" in response.json()["detail"].lower()

    def test_trigger_tts_nonexistent_script(self):
        """Test triggering TTS on nonexistent script returns 404."""
        response = client.post("/api/v1/tts/99999/synthesize")
        assert response.status_code == 404


class TestGetTTSTaskStatus:
    """Tests for GET /api/v1/tts/tasks/{task_id}."""

    def test_get_nonexistent_task_404(self):
        """Test getting a nonexistent TTS task returns 404."""
        response = client.get("/api/v1/tts/tasks/nonexistent-task-id")
        assert response.status_code == 404


class TestListTTSTasks:
    """Tests for GET /api/v1/tts/tasks."""

    def test_list_tts_tasks_empty(self):
        """Test listing TTS tasks when none exist."""
        response = client.get("/api/v1/tts/tasks")
        assert response.status_code == 200
        assert response.json() == []


# ── Config Endpoints ────────────────────────────────────────────

class TestConfigStatus:
    """Tests for GET /api/v1/config/status."""

    @patch("os.getenv", return_value="")
    def test_config_status_returns_features(self, mock_getenv: MagicMock):
        """Test that config status endpoint returns feature flags."""
        response = client.get("/api/v1/config/status")
        assert response.status_code == 200
        data = response.json()
        assert "features" in data
        assert "upload" in data["features"]
        assert data["features"]["upload"] is True
        assert "database_type" in data
        assert "max_file_size_mb" in data

    def test_config_status_with_api_key(self):
        """Test config status when API key is configured."""
        with patch.dict("os.environ", {"MOONSHOT_API_KEY": "sk-test-key"}, clear=False):
            response = client.get("/api/v1/config/status")
            assert response.status_code == 200
            data = response.json()
            assert data["moonshot_api_configured"] is True


class TestUpdateConfig:
    """Tests for POST /api/v1/config/."""

    @patch("app.api.endpoints.config.open")
    @patch("os.path.exists", return_value=True)
    @patch("os.getenv", return_value="")
    def test_update_config_sets_api_key(self, mock_getenv, mock_exists, mock_file):
        """Test that updating config returns success."""
        mock_file.return_value.__enter__.return_value.readlines.return_value = []
        mock_file.return_value.__enter__.return_value.writelines = MagicMock()

        response = client.post(
            "/api/v1/config/",
            json={"moonshot_api_key": "sk-new-key"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["moonshot_api_configured"] is True

    @patch("app.api.endpoints.config.open")
    @patch("os.path.exists", return_value=True)
    @patch("os.getenv", return_value="")
    def test_update_config_empty_key(self, mock_getenv, mock_exists, mock_file):
        """Test that updating config with empty key returns configured=false."""
        mock_file.return_value.__enter__.return_value.readlines.return_value = []
        mock_file.return_value.__enter__.return_value.writelines = MagicMock()

        response = client.post(
            "/api/v1/config/",
            json={"moonshot_api_key": ""},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["moonshot_api_configured"] is False


# ── General API Behavior ────────────────────────────────────────

class TestDocsEndpoint:
    """Tests for API documentation endpoints."""

    def test_docs_available(self):
        """Test that Swagger docs are accessible."""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_openapi_schema(self):
        """Test that OpenAPI schema is available."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "paths" in data
        assert "/health" in data["paths"]


class TestCORS:
    """Tests for CORS headers."""

    def test_cors_headers_present(self):
        """Test that CORS headers are present in responses."""
        response = client.get("/health")
        assert "access-control-allow-origin" in response.headers
