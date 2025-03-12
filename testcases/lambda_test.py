# Unit tests for lambda.py

```python
# Unit tests for the module handling GitHub PRs and code remediation

import unittest
from unittest.mock import patch, MagicMock
from your_module import get_open_prs, get_pr_changed_files, analyze_and_remediate_code, create_new_branch, comment_on_pr, rollback_main_branch, merge_remediated_branch, lambda_handler, invoke_bedrock_with_retry

class TestGitHubPRModule(unittest.TestCase):

    @patch('requests.get')
    def test_get_open_prs(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"number": 1, "title": "Test PR"}]
        result = get_open_prs("test_owner", "test_repo")
        self.assertEqual(result, [{"number": 1, "title": "Test PR"}])

    @patch('requests.get')
    def test_get_pr_changed_files(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"filename": "test.py"}]
        mock_raw_response = MagicMock()
        mock_raw_response.status_code = 200
        mock_raw_response.text = "print('test')"
        mock_get.side_effect = [mock_get.return_value, mock_raw_response]
        result = get_pr_changed_files("test_owner", "test_repo", 1)
        self.assertEqual(result, {"test.py": "print('test')"})

    @patch('your_module.invoke_bedrock_with_retry')
    def test_analyze_and_remediate_code(self, mock_bedrock):
        mock_bedrock.side_effect = [{"content": [{"text": "Issue 1"}, {"text": "Issue 2"}]}, {"content": [{"text": "Remediated code"}]}]
        code_repo = {"test.py": "def test(): pass"}
        result = analyze_and_remediate_code(code_repo)
        self.assertEqual(result, {"test.py": "Remediated code"})

    @patch('requests.get')
    @patch('requests.post')
    @patch('requests.patch')
    def test_create_new_branch(self, mock_patch, mock_post, mock_get):
        mock_get.side_effect = [MagicMock(status_code=200, json=lambda: {"object": {"sha": "base_sha"}}), MagicMock(status_code=404)]
        mock_post.side_effect = [MagicMock(status_code=201, json=lambda: {"sha": "blob_sha"}), MagicMock(status_code=201, json=lambda: {"sha": "tree_sha"}), MagicMock(status_code=201, json=lambda: {"sha": "commit_sha"})]
        mock_patch.return_value.status_code = 200
        remediations = {"test.py": "remediated code"}
        result = create_new_branch("test_owner", "test_repo", "main", "new_branch", remediations)
        self.assertEqual(result, "new_branch")

    @patch('requests.get')
    @patch('requests.post')
    def test_comment_on_pr(self, mock_post, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = []
        mock_post.return_value.status_code = 201
        comment_on_pr("test_owner", "test_repo", 1, "Test comment")
        mock_post.assert_called()

    @patch('requests.get')
    @patch('requests.patch')
    @patch('requests.delete')
    def test_rollback_main_branch(self, mock_delete, mock_patch, mock_get):
        mock_get.side_effect = [MagicMock(status_code=200, json=lambda: {"object": {"sha": "backup_sha"}}), Magic