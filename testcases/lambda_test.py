# Unit tests for the provided module

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import requests
import boto3
from botocore.exceptions import ClientError

from your_module import get_open_prs, get_pr_changed_files, analyze_and_remediate_code, create_new_branch, comment_on_pr, rollback_main_branch, merge_remediated_branch, lambda_handler, invoke_bedrock_with_retry

@pytest.fixture
def mock_requests():
    with patch('requests.get') as mock_get, patch('requests.post') as mock_post, patch('requests.patch') as mock_patch, patch('requests.delete') as mock_delete:
        yield mock_get, mock_post, mock_patch, mock_delete

@pytest.fixture
def mock_boto3():
    with patch('boto3.client') as mock_client:
        yield mock_client

def test_get_open_prs(mock_requests):
    mock_get, _, _, _ = mock_requests
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{"number": 1, "title": "Test PR"}]
    prs = get_open_prs("test_owner", "test_repo")
    assert prs == [{"number": 1, "title": "Test PR"}]

def test_get_pr_changed_files(mock_requests):
    mock_get, _, _, _ = mock_requests
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{"filename": "test.py"}]
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "print('Hello World')"
    files = get_pr_changed_files("test_owner", "test_repo", 1)
    assert files == {"test.py": "print('Hello World')"}

def test_analyze_and_remediate_code():
    code_repo = {"test.py": "print('Hello World')"}
    remediations = analyze_and_remediate_code(code_repo)
    assert remediations == {"test.py": "print('Hello World')"}

@patch('your_module.invoke_bedrock_with_retry')
def test_analyze_code(mock_invoke, mock_boto3):
    mock_invoke.return_value = {"content": [{"text": "No issues found"}]}
    code = "print('Hello World')"
    issues = analyze_code(code)
    assert issues == "No issues found"

@patch('your_module.invoke_bedrock_with_retry')
def test_remediate_code(mock_invoke, mock_boto3):
    mock_invoke.return_value = {"content": [{"text": "Remediated code"}]}
    code = "print('Hello World')"
    issues = ["Issue 1"]
    remediated_code = remediate_code(code, issues)
    assert remediated_code == "Remediated code"

def test_create_new_branch(mock_requests):
    mock_get, mock_post, _, _ = mock_requests
    mock_get.side_effect = [
        Mock(status_code=200, json=lambda: {"object": {"sha": "base_commit_sha"}}),
        Mock(status_code=404)
    ]
    mock_post.return_value.status_code = 201
    mock_post.return_value.json.return_value = {"sha": "blob_sha"}
    remediations = {"test.py": "print('Hello World')"}
    branch_name = create_new_branch("test_owner", "test_repo", "main", "new_branch", remediations)
    assert branch_name == "new_branch"

def test_comment_on_pr(mock_requests):
    mock_get, mock_post, _, _ = mock_requests
    mock_get.return_value.status_code = 200
    mock_get.return_value.