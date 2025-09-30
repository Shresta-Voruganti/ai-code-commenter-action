# AI Code Commenter GitHub Action

Automatically reviews pull requests and leaves helpful AI-generated comments on changed code using OpenAI GPT 🚀

This GitHub Action scans the code changes in a pull request, sends them to an OpenAI model, and posts structured, concise review comments — acting like an intelligent reviewer that helps improve code quality.

---

## ✨ Features

- 🧠 AI-generated code review comments on pull requests  
- ⚙️ Works with **any programming language**  
- 📁 Supports multi-file PRs (with optional batching to avoid rate limits)  
- 🔐 Secure – users bring their own OpenAI API key  
- ⚡️ Easy to integrate – just a few lines in your workflow

---

## 🚀 Usage

Add this workflow to your repository at:  
`.github/workflows/ai-commenter.yml`

```yaml
name: AI Code Commenter

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  ai-review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write

    steps:
      - uses: actions/checkout@v4

      - name: Run AI Code Commenter
        uses: Shresta-Voruganti/ai-code-commenter-action@main
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}       # ✅ Required for PR access
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}   # ✅ Your OpenAI API key
          MAX_BLOCKS: "3"                                 # ✅ Optional: max files to process

  ```

## 🔑 Setting up your OpenAI API Key

This action does **not** include an API key.
Each user must provide their own key as a GitHub Actions secret:

1. Go to your repository → **Settings → Secrets and variables → Actions**
2. Click **“New repository secret”**
3. Name: `OPENAI_API_KEY`
4. Value: *(your OpenAI API key from [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys))*

💡 **Tip:** A paid OpenAI API key is recommended for stable performance and higher rate limits.

---

## ⚙️ Optional Inputs

| Name         | Default | Description                                                              |
| ------------ | ------- | ------------------------------------------------------------------------ |
| `MAX_BLOCKS` | `5`     | Number of changed files to process per run. Reduce to avoid rate limits. |

---

## 🧠 Example Output

Once configured, the Action will automatically comment on pull requests, like:

> 🤖 **AI Review for `example.py`**
>
> * The function multiplies two numbers and returns the product.
> * Consider adding input validation to handle non-integer values.
> * Use more descriptive variable names for better readability.

---

## 🛠️ How It Works

1. 🧰 On each pull request, GitHub triggers this action.
2. 📁 The action scans changed files (up to `MAX_BLOCKS`).
3. 🔑 It sends each file’s diff to OpenAI GPT for analysis.
4. 💬 AI-generated review comments are posted directly on the PR.

---

## 💡 Notes

* ✅ Works with any language (`.py`, `.js`, `.java`, `.yml`, etc.)
* ⚠️ If using a free OpenAI key, you might hit rate limits. Paid keys are recommended.
* 🧪 You can adjust batching and `MAX_BLOCKS` in `main.py` for large PRs.

---

## 📦 Action Inputs Recap

| Env Variable     | Required | Description                                         |
| ---------------- | -------- | --------------------------------------------------- |
| `GITHUB_TOKEN`   | ✅ Yes    | GitHub-provided token for PR access (auto-injected) |
| `OPENAI_API_KEY` | ✅ Yes    | Your OpenAI API key (user-provided)                 |
| `MAX_BLOCKS`     | ❌ No     | Max number of files to process per run (default: 5) |

---

## 🤝 Contributing

Contributions are welcome! If you want to improve the review logic, prompt quality, or support more file types — feel free to open a PR.

---

## 📜 License

This project is licensed under the MIT License.

---

## 📌 Summary

* ✅ Users **don’t need your API key** — they add their own via `OPENAI_API_KEY`
* ✅ Your action is ready to be **publicly shared or used privately**
* ✅ Deployment is automatic when you push to `main`
* ✅ Anyone can integrate it with just a few lines in their workflow

---

### 🧪 Example Workflow Repository

You can see an example of how this Action is tested here:
👉 [test-ai-commenter-run](https://github.com/Shresta-Voruganti/test-ai-commenter-run)

---


