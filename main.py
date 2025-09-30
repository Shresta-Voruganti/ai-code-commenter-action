import os
import sys
import json
import openai
from github import Github

def get_changed_files():
    event_path = os.getenv('GITHUB_EVENT_PATH')
    if not event_path:
        print("GITHUB_EVENT_PATH not found")
        sys.exit(1)

    with open(event_path, 'r') as f:
        event_data = json.load(f)

    pr_number = event_data['pull_request']['number']
    repo = os.getenv('GITHUB_REPOSITORY')  # owner/repo format

    return repo, pr_number

def get_pr_changed_files(repo_name, pr_number):
    github_token = os.getenv('GITHUB_TOKEN')
    g = Github(github_token)

    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    changed_files = []
    for file in pr.get_files():
        if file.filename.endswith('.py'):
            changed_files.append({
                'filename': file.filename,
                'patch': file.patch
            })

    return changed_files

def extract_code_blocks(patch):
    lines = patch.split('\n')
    code_blocks = []
    current_block = []
    inside_function = False

    for line in lines:
        if line.startswith('+def ') or line.startswith('+class '):
            if current_block:
                code_blocks.append('\n'.join(current_block))
                current_block = []
            inside_function = True

        if inside_function:
            current_block.append(line[1:])  # Remove '+'

        if line.strip() == '':
            inside_function = False
            if current_block:
                code_blocks.append('\n'.join(current_block))
                current_block = []

    if current_block:
        code_blocks.append('\n'.join(current_block))

    return code_blocks

def generate_comment(openai_api_key, code_block):
    openai.api_key = openai_api_key
    prompt = f"Explain this Python code in simple terms:\n\n{code_block}\n\nExplanation:"

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0.5
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"OpenAI API error: {str(e)}")
        return None

def format_comment(filename, explanation):
    return f"### 🤖 AI Code Commenter\n\n**File:** `{filename}`\n\n> {explanation}"

def post_comment(repo_name, pr_number, comment_body):
    github_token = os.getenv('GITHUB_TOKEN')
    g = Github(github_token)

    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    pr.create_issue_comment(comment_body)

def main():
    openai_api_key = os.getenv('INPUT_OPENAI_API_KEY')
    max_blocks = int(os.getenv('INPUT_MAX_BLOCKS', 5))

    repo, pr_number = get_changed_files()
    changed_files = get_pr_changed_files(repo, pr_number)

    for file in changed_files:
        code_blocks = extract_code_blocks(file['patch'])[:max_blocks]

        for block in code_blocks:
            explanation = generate_comment(openai_api_key, block)
            if explanation:
                comment = format_comment(file['filename'], explanation)
                post_comment(repo, pr_number, comment)

if __name__ == "__main__":
    main()

