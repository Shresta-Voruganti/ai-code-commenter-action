# AI-Powered Code Commenter GitHub Action

This GitHub Action automatically comments code logic in your pull requests using OpenAI GPT API.

## ✅ Usage

```yaml
name: Auto Comment Code
on: [pull_request]

jobs:
  ai_commenter:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run AI Code Commenter
        uses: your-username/ai-code-commenter-action@v1
        with:
          openai_api_key: ${{ secrets.OPENAI_API_KEY }}
          max_blocks: 5

