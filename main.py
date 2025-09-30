import os
import json
import requests
from github import Github

def get_pr_number_from_event():
    """Extract PR number from GitHub event JSON."""
    event_path = os.getenv("GITHUB_EVENT_PATH")
    if event_path and os.path.exists(event_path):
        with open(event_path, "r") as f:
            event = json.load(f)
        pr = event.get("pull_request")
        if pr:
            return pr.get("number")
    return None

def call_openai_review(api_key, filename, patch):
    """Send the patch to OpenAI and get a review comment."""
    if not patch:
        return None

    prompt = f"""You are a senior code reviewer.
Review the changes made in the file `{filename}` below and write 4–6 helpful, concise review comments.
Focus on explaining what the code does and suggesting improvements if needed.

Code diff:
{patch}
"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 400,
        "temperature": 0.2
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()

def main():
    print("=== 🤖 AI Code Commenter (Real Mode) ===")

    # Get environment variables
    repo_name = os.getenv("GITHUB_REPOSITORY")
    github_token = os.getenv("GITHUB_TOKEN")
    openai_key = os.getenv("OPENAI_API_KEY")
    pr_number = get_pr_number_from_event()
    max_blocks = int(os.getenv("MAX_BLOCKS", "5"))

    # Debug info
    print("📦 Repo:", repo_name)
    print("🔢 PR Number:", pr_number)
    print("🔑 GitHub Token Provided:", bool(github_token))
    print("🔑 OpenAI Key Provided:", bool(openai_key))

    # Validate inputs
    if not all([repo_name, github_token, openai_key, pr_number]):
        raise RuntimeError("❌ Missing one or more required environment variables.")

    # Authenticate with GitHub
    gh = Github(github_token)
    repo = gh.get_repo(repo_name)
    pr = repo.get_pull(int(pr_number))

    print("📂 Fetching changed files...")
    files = list(pr.get_files())
    print(f"Found {len(files)} changed files.")

    for i, f in enumerate(files[:max_blocks]):
        print(f"🧠 Processing file {i+1}: {f.filename}")
        review_comment = call_openai_review(openai_key, f.filename, f.patch)

        if review_comment:
            body = f"**🤖 AI Review for `{f.filename}`:**\n\n{review_comment}"
            pr.create_issue_comment(body)
            print(f"✅ Posted comment for {f.filename}")
        else:
            print(f"⚠️ No comment generated for {f.filename}")

    print("🎉 All done — AI comments have been posted on the PR!")

if __name__ == "__main__":
    main()

