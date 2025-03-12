# Unit tests for the GitHub PR remediation module

import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from main import app  # Assuming the module is imported as 'main'

client = TestClient(app)

@pytest.fixture
def mock_bedrock():
    with patch('main.bedrock.invoke_model') as mock:
        yield mock

@pytest.fixture
def mock_requests():
    with patch('requests.get') as mock:
        yield mock

def test_get_open_prs(mock_requests):
    mock_requests.return_value.status_code = 200
    mock_requests.return_value.json.return_value = [{"number": 1, "title": "Test PR"}]
    response = client.get("/get_open_prs?owner=test&repo=test")
    assert response.status_code == 200
    assert response.json() == [{"number": 1, "title": "Test PR"}]

def test_get_pr_changed_files(mock_requests):
    mock_requests.return_value.status_code = 200
    mock_requests.return_value.json.return_value = [{"filename": "test.py"}]
    response = client.get("/get_pr_changed_files?owner=test&repo=test&pr_number=1")
    assert response.status_code == 200
    assert "test.py" in response.json()

def test_analyze_and_remediate_code(mock_bedrock):
    mock_bedrock.return_value = {"content": [{"text": "Issue found"}]}
    code_repo = {"test.py": "def test(): pass"}
    result = client.post("/analyze_and_remediate_code", json=code_repo)
    assert result.status_code == 200
    assert "test.py" in result.json()

def test_create_new_branch(mock_requests):
    mock_requests.return_value.status_code = 201
    remediations = {"test.py": "remediated code"}
    response = client.post("/create_new_branch", json={"owner": "test", "repo": "test", "base_branch": "main", "new_branch_name": "remediation", "remediations": remediations})
    assert response.status_code == 200
    assert "remediation" in response.json()

def test_comment_on_pr(mock_requests):
    mock_requests.return_value.status_code = 201
    response = client.post("/comment_on_pr", json={"owner": "test", "repo": "test", "pr_number": 1, "comments": "Test comment"})
    assert response.status_code == 200

def test_rollback_main_branch(mock_requests):
    mock_requests.return_value.status_code = 200
    response = client.post("/rollback_main_branch", json={"owner": "test", "repo": "test", "backup_branch": "backup", "faulty_branch": "faulty"})
    assert response.status_code == 200

def test_merge_remediated_branch(mock_requests):
    mock_requests.return_value.status_code = 201
    response = client.post("/merge_remediated_branch", json={"owner": "test", "repo": "test", "base_branch": "main", "new_branch": "remediation", "pr_number": 1})
    assert response.status_code == 200

def test_lambda_handler(mock_requests, mock_bedrock):
    mock_requests.return_value.status_code = 200
    mock_bedrock.return_value = {"content": [{"text": "Issue found"}]}
    response = client.post("/lambda_handler", json={"actionGroup": "test", "parameters": [{"name": "owner", "value": "test"}, {"name": "repo", "value": "test"}]})
    assert response.status_code == 200