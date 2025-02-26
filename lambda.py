import json
import logging
import base64
import os
import boto3
import re
import requests
from urllib.parse import urlparse
import botocore.exceptions
import time
import random

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize a Boto3 client for Bedrock
bedrock = boto3.client(service_name='bedrock-runtime', region_name="us-west-2")

GITHUB_API_URL = "https://api.github.com"

# Fetch the GitHub token from environment variables
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    raise ValueError("GitHub token is not set in the environment variables")

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Content-Type": "application/json"
}

def get_open_prs(owner, repo):
    """Fetch all open PRs for the repository."""
    api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls?state=open"
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    return [{"number": pr["number"], "title": pr["title"]} for pr in response.json()]

def get_pr_changed_files(owner, repo, pr_number):
    """Fetch the list of changed Python files in a PR and get full file content."""
    api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()

    print("----> get_pr_changed_files")
    print(response)

    changed_files = {}
    for file in response.json():
        file_path = file["filename"]
        if file_path.endswith(".py"):  # Process only Python files
            # Fetch full file content from GitHub
            raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/{file_path}"
            file_response = requests.get(raw_url, headers=headers)

            if file_response.status_code == 200:
                changed_files[file_path] = file_response.text
            else:
                print(f"Failed to fetch {file_path}: {file_response.text}")
    
    print("----> changed_files")
    print(changed_files)

    return changed_files

def analyze_and_remediate_code(code_repo):
    """Analyze and remediate the full Python file."""
    remediations = {}

    for file_path, full_code in code_repo.items():
        issues = analyze_code(full_code)  # Analyze full file
        if issues:
            remediated_code = remediate_code(full_code, issues.split("\n"))
            remediations[file_path] = remediated_code
        else:
            remediations[file_path] = full_code  # No changes needed

    return remediations

def analyze_code(code):
    messages = [
        {"role": "user", "content": f"Analyze the following code changes and list any issues:\n\n{code}"}
    ]

    response = invoke_bedrock_with_retry(messages)
    
    if not response or "content" not in response:
        raise ValueError("Invalid response from Bedrock API: Missing 'content' field")

    # ✅ Extract and join text responses
    content_list = response.get("content", [])
    if not isinstance(content_list, list):
        raise ValueError("Unexpected response format from Bedrock API")

    return "\n".join([item["text"] for item in content_list if "text" in item]).strip()


def remediate_code(code, issues):
    """Remediate the detected issues in the code."""
    messages = [
        {"role": "user", "content": "You are a coding assistant that fixes issues in the given code."},
        {"role": "user", "content": f"Fix the following issues in this code:\n\n{code}\n\nIssues:\n{', '.join(issues)}"}
    ]

    response = invoke_bedrock_with_retry(messages)

    if not response or "content" not in response:
        raise ValueError("Invalid response from Bedrock API: Missing 'content' field")

    # ✅ Extract and join text responses
    content_list = response.get("content", [])
    if not isinstance(content_list, list):
        raise ValueError("Unexpected response format from Bedrock API")

    return "\n".join([item["text"] for item in content_list if "text" in item]).strip()

def create_new_branch(owner, repo, base_branch, new_branch_name, remediations):
    """Create a new branch with the remediated code and push changes to GitHub."""

    base_commit_url = f"https://api.github.com/repos/{owner}/{repo}/git/refs/heads/{base_branch}"
    response = requests.get(base_commit_url, headers=headers)
    response.raise_for_status()
    base_commit = response.json()["object"]["sha"]

    new_branch_url = f"https://api.github.com/repos/{owner}/{repo}/git/refs"
    
    # Check if branch already exists
    existing_branch_response = requests.get(f"{new_branch_url}/heads/{new_branch_name}", headers=headers)
    if existing_branch_response.status_code == 200:
        timestamp = int(time.time())
        new_branch_name = f"{new_branch_name}-{timestamp}"
        logger.info(f"Branch already exists. Creating a new unique branch: {new_branch_name}")

    # Create new branch
    response = requests.post(new_branch_url, json={"ref": f"refs/heads/{new_branch_name}", "sha": base_commit}, headers=headers)
    response.raise_for_status()

    # Create blobs and commit changes
    blobs = []
    for file_path, remediated_code in remediations.items():
        blob_payload = {
            "content": base64.b64encode(remediated_code.encode()).decode(),
            "encoding": "base64"
        }
        blob_url = f"https://api.github.com/repos/{owner}/{repo}/git/blobs"
        response = requests.post(blob_url, json=blob_payload, headers=headers)
        response.raise_for_status()
        blob_sha = response.json()["sha"]
        blobs.append({"path": file_path, "mode": "100644", "type": "blob", "sha": blob_sha})

    base_tree_sha = requests.get(f"https://api.github.com/repos/{owner}/{repo}/git/trees/{base_commit}", headers=headers).json()["sha"]
    new_tree_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees"
    new_tree_sha = requests.post(new_tree_url, json={"base_tree": base_tree_sha, "tree": blobs}, headers=headers).json()["sha"]

    commit_url = f"https://api.github.com/repos/{owner}/{repo}/git/commits"
    new_commit_sha = requests.post(commit_url, json={"message": "Remediated code", "tree": new_tree_sha, "parents": [base_commit]}, headers=headers).json()["sha"]

    response = requests.patch(f"{new_branch_url}/heads/{new_branch_name}", json={"sha": new_commit_sha}, headers=headers)
    response.raise_for_status()

    return new_branch_name

def comment_on_pr(owner, repo, pr_number, comments, max_retries=3):
    """Post structured comments on a GitHub PR, avoiding duplicates and handling errors."""
    comment_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"

    # Fetch existing comments to prevent duplicates
    existing_comments_response = requests.get(comment_url, headers=headers)
    if existing_comments_response.status_code == 200:
        existing_comments = [comment["body"] for comment in existing_comments_response.json()]
        if comments in existing_comments:
            logger.info(f"Skipping duplicate comment on PR #{pr_number}")
            return

    # 📝 Improve comment formatting
    formatted_comment = f"""
###
The following issues were detected and have been addressed automatically:

{comments}

---
_This review was generated by an AI-powered analysis system._
"""

    payload = {"body": formatted_comment}
    
    for attempt in range(max_retries):
        response = requests.post(comment_url, headers=headers, json=payload)
        
        if response.status_code == 201:
            logger.info(f"Successfully commented on PR #{pr_number}")
            return
        elif response.status_code == 403 and "X-RateLimit-Remaining" in response.headers:
            # Handle API rate limiting (if applicable)
            rate_limit_reset = int(response.headers.get("X-RateLimit-Reset", time.time()))
            wait_time = max(rate_limit_reset - int(time.time()), 1)
            logger.warning(f"GitHub API rate limit exceeded. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        else:
            logger.error(f"Failed to comment on PR #{pr_number} (Attempt {attempt+1}): {response.text}")

    logger.error(f"Unable to post comment on PR #{pr_number}.")


def rollback_main_branch(owner, repo, backup_branch, faulty_branch):
    """Rollback main branch to the backup commit if the merge fails."""
    logger.warning(f"Rolling back main branch to backup: {backup_branch}")

    # Step 1: Get latest commit SHA of the backup branch
    backup_commit_url = f"https://api.github.com/repos/{owner}/{repo}/git/ref/heads/{backup_branch}"
    response = requests.get(backup_commit_url, headers=headers)

    if response.status_code != 200:
        logger.error(f"Failed to retrieve backup branch {backup_branch}: {response.text}")
        return

    backup_commit_sha = response.json()["object"]["sha"]

    # Step 2: Force update main branch to backup commit
    update_main_url = f"https://api.github.com/repos/{owner}/{repo}/git/refs/heads/main"
    reset_payload = {"sha": backup_commit_sha, "force": True}
    response = requests.patch(update_main_url, json=reset_payload, headers=headers)

    if response.status_code == 200:
        logger.info(f"Successfully rolled back main to {backup_commit_sha}")
    else:
        logger.error(f"Rollback failed: {response.text}")
        return

    # Step 3: Delete the faulty remediation branch
    delete_branch_url = f"https://api.github.com/repos/{owner}/{repo}/git/refs/heads/{faulty_branch}"
    response = requests.delete(delete_branch_url, headers=headers)

    if response.status_code == 204:
        logger.info(f"Deleted faulty branch {faulty_branch} after rollback")
    else:
        logger.warning(f"Failed to delete faulty branch {faulty_branch}: {response.text}")

def merge_remediated_branch(owner, repo, base_branch, new_branch, pr_number):
    """Create a PR for the remediated branch, backup main, and merge."""
    
    timestamp = int(time.time())
    backup_branch = f"backup-{base_branch}-{timestamp}"
    
    # Step 1: Get latest commit SHA of base branch (main)
    base_commit_url = f"https://api.github.com/repos/{owner}/{repo}/git/refs/heads/{base_branch}"
    response = requests.get(base_commit_url, headers=headers)
    response.raise_for_status()
    base_commit_sha = response.json()["object"]["sha"]

    # Step 2: Create a backup branch before merging
    backup_url = f"https://api.github.com/repos/{owner}/{repo}/git/refs"
    backup_payload = {"ref": f"refs/heads/{backup_branch}", "sha": base_commit_sha}
    backup_response = requests.post(backup_url, json=backup_payload, headers=headers)
    
    if backup_response.status_code == 201:
        logger.info(f"Backup branch {backup_branch} created successfully.")
    else:
        logger.error(f"Failed to create backup branch {backup_branch}: {backup_response.text}")
        return

    # Step 3: Create a PR for the remediation branch
    pr_url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    commit_message = f"Remediated code for PR #{pr_number}: Fixed identified issues in changed files."

    pr_payload = {
        "title": f"Remediated Fixes for PR #{pr_number}",
        "head": new_branch,
        "base": base_branch,
        "body": commit_message
    }
    
    response = requests.post(pr_url, headers=headers, json=pr_payload)
    
    if response.status_code == 201:
        pr_data = response.json()
        new_pr_number = pr_data["number"]
        merge_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_data['number']}/merge"
        merge_response = requests.put(merge_url, headers=headers, json={"commit_message": commit_message})

        if merge_response.status_code == 200:
            logger.info(f"Successfully merged remediation branch {new_branch} into {base_branch}")
            # ✅ **CLOSE THE ORIGINAL PR AFTER MERGE**
            close_pr_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
            close_payload = {"state": "closed"}
            close_response = requests.patch(close_pr_url, headers=headers, json=close_payload)

            if close_response.status_code == 200:
                logger.info(f"Successfully closed original PR #{pr_number}")
            else:
                logger.error(f"Failed to close original PR #{pr_number}: {close_response.text}")
        else:
            logger.error(f"Failed to merge branch {new_branch}: {merge_response.text}")
    else:
        logger.error(f"Failed to create PR for remediation branch {new_branch}: {response.text}")


def lambda_handler(event, context):
    try:
        actionGroup = event['actionGroup']
        parameters = {param["name"]: param["value"] for param in event.get('parameters', [])}

        owner = parameters.get('owner')
        repo = parameters.get('repo')
        new_branch_name = parameters.get('new_remediated_branch_name', "remediation")

        if not owner or not repo:
            raise ValueError("Missing required parameters: 'owner' or 'repo'.")

        open_prs = get_open_prs(owner, repo)
        if not open_prs:
        
            return {
            "response": {
            "actionGroup": "PR_review_commit_merge",
            "functionResponse": {
                "responseBody": {
                    "TEXT": {
                        "body": "No open PRs found"
                    }
                }
            }
        },
        "messageVersion": "1.0"
    }
        results = {}

        new_branch = None  # Initialize before loop
        for pr in open_prs:
            pr_number = pr["number"]
            new_branch_name_with_pr = f"{new_branch_name}-{pr_number}"
            code_repo = get_pr_changed_files(owner, repo, pr_number)
            remediations = analyze_and_remediate_code(code_repo)
            issue_details = "\n".join([f"- {issue}" for issue in remediations.values()])
            comment_message = f"### Automated Code Review Findings\n{issue_details}"
            comment_on_pr(owner, repo, pr_number, comment_message)
            new_branch = create_new_branch(owner, repo, "main", new_branch_name_with_pr, remediations)
            merge_remediated_branch(owner, repo, "main", new_branch, pr_number)
            results[pr_number] = new_branch

        responseBody = {"TEXT": {"body": new_branch if new_branch else "No new branch created"}}

        return {'response': {'actionGroup': actionGroup, 'functionResponse': {'responseBody': responseBody}}, 'messageVersion': event.get('messageVersion', '1.0')}

    except Exception as e:
        logger.error("An error occurred: %s", e, exc_info=True)
        return {'response': {'actionGroup': event.get('actionGroup', ''), 'functionResponse': {'responseBody': {"TEXT": {"body": f"Error: {str(e)}"}}}}, 'messageVersion': event.get('messageVersion', '1.0')}

def invoke_bedrock_with_retry(messages, max_retries=5):
    for attempt in range(max_retries):
        try:
            payload = {
                "anthropic_version": "bedrock-2023-05-31",  # ✅ Required field
                "messages": messages,
                "max_tokens": 500,
                "temperature": 0.7,
                "top_p": 0.9
            }

            response = bedrock.invoke_model(
                modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
                contentType="application/json",
                accept="application/json",
                body=json.dumps(payload)
            )

            if not response or "body" not in response:
                raise ValueError("Invalid response from Bedrock API: Missing 'body' field")

            response_body = response["body"].read()
            if not response_body:
                raise ValueError("Invalid response from Bedrock API: Response body is empty")

            return json.loads(response_body)

        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "ThrottlingException":
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                print(f"Throttled. Retrying in {wait_time:.2f} seconds...")
                time.sleep(wait_time)
            else:
                raise  # Re-raise if it's not a throttling error

    raise Exception("Max retries reached for AWS Bedrock API")



