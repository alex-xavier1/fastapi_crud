# Unit test for the remediation module

import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from main import app  # Assuming the module is imported in a FastAPI app

client = TestClient(app)

@pytest.fixture
def mock_bedrock():
    with patch('boto3.client') as boto_mock:
        bedrock_mock = boto_mock.return_value
        bedrock_mock.invoke_model.return_value = {
            'body': '{"content": [{"text": "Issue 1"}, {"text": "Issue 2"}]}'.encode('utf-8')
        }
        yield bedrock_mock

@pytest.fixture
def mock_requests():
    with patch('requests.get') as get_mock, patch('requests.post') as post_mock, patch('requests.patch') as patch_mock, patch('requests.delete') as delete_mock:
        get_mock.return_value.status_code = 200
        get_mock.return_value.json.return_value = {"object": {"sha": "base_sha"}}
        post_mock.return_value.status_code = 201
        post_mock.return_value.json.return_value = {"sha": "new_sha"}
        patch_mock.return_value.status_code = 200
        delete_mock.return_value.status_code = 204
        yield get_mock, post_mock, patch_mock, delete_mock

def test_get_open_prs(mock_requests):
    get_mock, _, _, _ = mock_requests
    response = client.get("/get_open_prs?owner=test_owner&repo=test_repo")
    assert response.status_code == 200
    get_mock.assert_called()

def test_get_pr_changed_files(mock_requests):
    get_mock, _, _, _ = mock_requests
    response = client.get("/get_pr_changed_files?owner=test_owner&repo=test_repo&pr_number=1")
    assert response.status_code == 200
    get_mock.assert_called()

def test_analyze_and_remediate_code(mock_bedrock):
    code_repo = {"test.py": "print('Hello, world!')"}
    remediations = client.post("/analyze_and_remediate_code", json=code_repo)
    assert remediations.status_code == 200

def test_create_new_branch(mock_requests):
    _, post_mock, _, _ = mock_requests
    response = client.post("/create_new_branch", json={"owner": "test_owner", "repo": "test_repo", "base_branch": "main", "new_branch_name": "new_branch", "remediations": {"test.py": "remediated_code"}})
    assert response.status_code == 200
    post_mock.assert_called()

def test_comment_on_pr(mock_requests):
    _, post_mock, _, _ = mock_requests
    response = client.post("/comment_on_pr", json={"owner": "test_owner", "repo": "test_repo", "pr_number": 1, "comments": "Test comment"})
    assert response.status_code == 200
    post_mock.assert_called()

def test_rollback_main_branch(mock_requests):
    _, _, patch_mock, delete_mock = mock_requests
    response = client.post("/rollback_main_branch", json={"owner": "test_owner", "repo": "test_repo", "backup_branch": "backup", "faulty_branch": "faulty"})
    assert response.status_code == 200
    patch_mock.assert_called()
    delete_mock.assert_called()

def test_merge_remediated_branch(mock_requests):
    _, post_mock, _, _ = mock_requests
    response = client.post("/merge_remediated_branch", json={"owner": "test_owner", "repo": "test_repo",