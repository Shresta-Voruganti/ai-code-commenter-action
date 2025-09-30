import os, json

def main():
    repo = os.getenv("GITHUB_REPOSITORY")
    event_name = os.getenv("GITHUB_EVENT_NAME")
    event_path = os.getenv("GITHUB_EVENT_PATH")
    openai_key = os.getenv("OPENAI_API_KEY") or os.getenv("INPUT_OPENAI_API_KEY")
    max_blocks = os.getenv("MAX_BLOCKS") or os.getenv("INPUT_MAX_BLOCKS") or "5"

    print("=== AI Code Commenter (simulation) ===")
    print(f"Repo: {repo}")
    print(f"Event: {event_name}")
    print(f"OPENAI key provided? {'yes' if openai_key else 'no'}")
    print(f"max_blocks = {max_blocks}")

    pr_number = None
    if event_path and os.path.exists(event_path):
        with open(event_path, "r") as f:
            evt = json.load(f)
        pr = evt.get("pull_request") if isinstance(evt, dict) else None
        if pr:
            pr_number = pr.get("number")
    print(f"PR number: {pr_number}")

    # Simulate “changed files”
    files = ["example.py"]
    print(f"files to process: {len(files)} -> {files}")

    for f in files[:int(max_blocks)]:
        print("-" * 60)
        print(f"🤖 (simulated) would analyze `{f}` and post helpful comments")

    print("Simulation done ✅")

if __name__ == "__main__":
    main()

